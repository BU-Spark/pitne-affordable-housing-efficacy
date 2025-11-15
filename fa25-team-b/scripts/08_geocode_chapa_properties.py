from __future__ import annotations
# 08_geocode_chapa_properties.py
#
# 1) Load CHAPA properties from chapa_properties_from_apps.csv
# 2) Geocode them (lat/lon) with caching + cleaning/fallbacks
# 3) Merge property coords into applications_clean.parquet
# 4) Save applications_with_property_geo.parquet + CSV

from pathlib import Path
import time
import re

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


# ---------- paths ----------
BASE_DIR = Path(__file__).resolve().parents[1]   # fa25-team-b/
DATA_DIR = BASE_DIR / "data"
PROCESSED = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"

APPS_FILE = PROCESSED / "applications_clean.parquet"
PROPS_FILE = PROCESSED / "chapa_properties_from_apps.csv"
PROP_CACHE_FILE = CACHE_DIR / "property_geocode.parquet"
OUT_FILE = PROCESSED / "applications_with_property_geo.parquet"
OUT_CSV = PROCESSED / "applications_with_property_geo.csv"   # <- NEW


# ---------- helpers ----------

def _normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def split_property(prop: str) -> tuple[str, str]:
    """
    Split 'Application Property' into (street, city) and clean junk.

    Handles patterns like:
        '1 Harvest Drive Unit 110 ~ North Andover'
        '100 Franklin Street, #A1 ~ Whitman'
        '2 Marys Way ~ Lakeville (age restricted)'
        'Falmouth - (age restricted) 110 Dillingham'
        'West Boylston - 103 Afra Drive Unit 51'
        'Groton, 503 Main'
        '6 Woodman Way, Unit 317A'
    """
    if prop is None or (isinstance(prop, float) and np.isnan(prop)):
        return "", ""

    s = str(prop).strip()

    # 1) Remove everything in parentheses: "(55+)", "(first come...)", "(age restricted)", etc.
    s = re.sub(r"\([^)]*\)", "", s)

    # 2) Normalize multiple commas and spaces
    s = s.replace(",,", ",")
    s = _normalize_spaces(s)

    # 3) If there is a "~", assume "street ~ city"
    #    e.g. "1 Harvest Drive Unit 110 ~ North Andover"
    if "~" in s:
        street, city = [_normalize_spaces(x) for x in s.split("~", 1)]
        return street.strip(", "), city.strip(", ")

    # 4) Pattern: "City, 503 Main"
    #    e.g. "Groton, 503 Main"
    m_city_comma = re.match(r"^([A-Za-z .'-]+),\s*(\d.+)$", s)
    if m_city_comma:
        city = _normalize_spaces(m_city_comma.group(1))
        street = _normalize_spaces(m_city_comma.group(2))
        return street.strip(", "), city.strip(", ")

    # 5) Pattern: "City - something with numbers"
    #    e.g. "Falmouth - 110 Dillingham", "West Boylston - 103 Afra Drive Unit 51"
    m_city_dash = re.match(r"^([A-Za-z .'-]+)\s*-\s*(.+)$", s)
    if m_city_dash and re.search(r"\d", m_city_dash.group(2)):
        city = _normalize_spaces(m_city_dash.group(1))
        street = _normalize_spaces(m_city_dash.group(2))
        return street.strip(", "), city.strip(", ")

    # 6) Otherwise, treat the whole thing as street with unknown city
    #    e.g. "1 Ashley Lane, Unit 50"
    return s.strip(", "), ""


def build_query_variants(street: str, city: str) -> list[str]:
    """
    Given cleaned (street, city), build several query variants
    from most specific to more generic, to improve geocoding success.
    """
    variants: list[str] = []

    street = street.strip(", ")
    city = city.strip(", ")

    # Most specific: full street + city
    if street and city:
        variants.append(f"{street}, {city}, Massachusetts, USA")
    elif street:
        variants.append(f"{street}, Massachusetts, USA")

    # Remove "Unit XXX" and "#XXX" from the street
    street_no_unit = re.sub(r"Unit\s+\S+", "", street)
    street_no_unit = re.sub(r"#\S+", "", street_no_unit)
    street_no_unit = _normalize_spaces(street_no_unit).strip(", ")

    if street_no_unit and street_no_unit != street:
        if city:
            variants.append(f"{street_no_unit}, {city}, Massachusetts, USA")
        else:
            variants.append(f"{street_no_unit}, Massachusetts, USA")

    # City-only fallback (rough centroid, but better than missing)
    if city:
        variants.append(f"{city}, Massachusetts, USA")

    # De-duplicate while preserving order
    seen = set()
    cleaned = []
    for q in variants:
        if q not in seen and q.strip():
            seen.add(q)
            cleaned.append(q)
    return cleaned


def geocode_chapa_properties(properties: pd.Series) -> pd.DataFrame:
    """
    Geocode CHAPA properties to lat/lon with caching.

    Returns columns:
        - Application Property
        - property_latitude
        - property_longitude
        - property_full_location_name
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if PROP_CACHE_FILE.exists():
        cache = pd.read_parquet(PROP_CACHE_FILE)
        print(f"📦 Loaded existing property cache: {PROP_CACHE_FILE}")
    else:
        cache = pd.DataFrame(
            columns=[
                "Application Property",
                "property_latitude",
                "property_longitude",
                "property_full_location_name",
            ]
        )

    # Only treat rows with non-null coords as "known" (failed ones get retried)
    if not cache.empty:
        ok_mask = cache["property_latitude"].notna() & cache["property_longitude"].notna()
        known = set(cache.loc[ok_mask, "Application Property"].astype(str))
    else:
        known = set()

    props_clean = [p for p in properties if pd.notna(p)]
    to_geocode = sorted(set(str(p) for p in props_clean) - known)

    if not to_geocode:
        print("   (no new properties to geocode, using cache only)")
        return cache

    print(f"🌍 Need to geocode {len(to_geocode)} new properties")
    geolocator = Nominatim(user_agent="chapa_property_coords", timeout=20)
    new_rows = []

    for i, prop in enumerate(to_geocode, start=1):
        street, city = split_property(prop)
        queries = build_query_variants(street, city)

        lat = lon = addr = None
        success = False

        for q in queries:
            try:
                loc = geolocator.geocode(q)
                if loc:
                    lat, lon, addr = loc.latitude, loc.longitude, loc.address
                    print(f"[{i}/{len(to_geocode)}] OK   -> {q}")
                    success = True
                    break
            except Exception as e:
                print(f"[{i}/{len(to_geocode)}] ERROR -> {q} ({e})")

            # Polite to Nominatim
            time.sleep(1.2)

        if not success:
            print(f"[{i}/{len(to_geocode)}] FAIL (all variants) -> {prop}")

        new_rows.append(
            {
                "Application Property": str(prop),
                "property_latitude": lat,
                "property_longitude": lon,
                "property_full_location_name": addr,
            }
        )

    new_df = pd.DataFrame(new_rows)

    if cache.empty:
        out = new_df
    else:
        out = pd.concat([cache, new_df], ignore_index=True)

    out = out.drop_duplicates("Application Property", keep="last")
    out.to_parquet(PROP_CACHE_FILE, index=False)
    print(f"💾 Saved/updated property cache: {PROP_CACHE_FILE}")
    return out


# ---------- main ----------
def main():
    # 0) Load applications
    if not APPS_FILE.exists():
        raise SystemExit(f"Missing {APPS_FILE}")

    print(f"📄 Loading applications: {APPS_FILE}")
    apps = pd.read_parquet(APPS_FILE)
    print(f"   rows={len(apps):,}, cols={len(apps.columns)}")

    if "Application Property" not in apps.columns:
        raise SystemExit("Column 'Application Property' not found in applications_clean.parquet")

    # 1) Load CHAPA properties from precomputed CSV (07_find_chapa_properties.py)
    if not PROPS_FILE.exists():
        raise SystemExit(
            f"Missing property file: {PROPS_FILE}. "
            "Run scripts/07_find_chapa_properties.py first."
        )

    props_df = pd.read_csv(PROPS_FILE)

    if "Application Property" not in props_df.columns:
        raise SystemExit(
            "Column 'Application Property' not found in chapa_properties_from_apps.csv"
        )

    props = (
        props_df["Application Property"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    print(f"🏠 Unique CHAPA properties (from CSV): {len(props)}")

    # 2) Geocode properties (with caching)
    geo = geocode_chapa_properties(props)

    # 3) Merge property coordinates into applications
    merge_cols = [
        "Application Property",
        "property_latitude",
        "property_longitude",
        "property_full_location_name",
    ]
    apps_geo = apps.merge(geo[merge_cols], on="Application Property", how="left")
    print("🔗 Property coordinates merged into applications.")

    # 4) Save result (no distance column – Pavlo can add distance from these coords)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    apps_geo.to_parquet(OUT_FILE, index=False)
    apps_geo.to_csv(OUT_CSV, index=False)   # <- NEW

    print("\n✅ Done. Output written to:")
    print(f"   {OUT_FILE}")
    print(f"   {OUT_CSV}")


if __name__ == "__main__":
    main()
