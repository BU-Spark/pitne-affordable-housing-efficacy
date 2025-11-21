import time
import re
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

def _normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def split_property(prop: str) -> tuple[str, str]:
    if prop is None or (isinstance(prop, float) and np.isnan(prop)):
        return "", ""

    s = str(prop).strip()
    s = re.sub(r"\([^)]*\)", "", s)       # remove parentheses
    s = s.replace(",,", ",")
    s = _normalize_spaces(s)

    # "~" → (street, city)
    if "~" in s:
        street, city = [_normalize_spaces(x) for x in s.split("~", 1)]
        return street.strip(", "), city.strip(", ")

    # "City, 503 Main"
    m_city_comma = re.match(r"^([A-Za-z .'-]+),\s*(\d.+)$", s)
    if m_city_comma:
        city = _normalize_spaces(m_city_comma.group(1))
        street = _normalize_spaces(m_city_comma.group(2))
        return street.strip(", "), city.strip(", ")

    # "City - 103 Something"
    m_city_dash = re.match(r"^([A-Za-z .'-]+)\s*-\s*(.+)$", s)
    if m_city_dash and re.search(r"\d", m_city_dash.group(2)):
        city = _normalize_spaces(m_city_dash.group(1))
        street = _normalize_spaces(m_city_dash.group(2))
        return street.strip(", "), city.strip(", ")

    return s.strip(", "), ""


def build_query_variants(street: str, city: str) -> list[str]:
    variants = []
    street = street.strip(", ")
    city = city.strip(", ")

    # Most specific
    if street and city:
        variants.append(f"{street}, {city}, Massachusetts, USA")
    elif street:
        variants.append(f"{street}, Massachusetts, USA")

    # Remove unit/apartment indicators
    street_no_unit = re.sub(r"Unit\s+\S+", "", street)
    street_no_unit = re.sub(r"#\S+", "", street_no_unit)
    street_no_unit = _normalize_spaces(street_no_unit).strip(", ")

    if street_no_unit and street_no_unit != street:
        if city:
            variants.append(f"{street_no_unit}, {city}, Massachusetts, USA")
        else:
            variants.append(f"{street_no_unit}, Massachusetts, USA")

    # City-only fallback
    if city:
        variants.append(f"{city}, Massachusetts, USA")

    # unique in order
    seen, cleaned = set(), []
    for q in variants:
        if q not in seen and q.strip():
            seen.add(q)
            cleaned.append(q)

    return cleaned

def applicant_property_geocoding(df: pd.DataFrame) -> pd.DataFrame:
    """
        Takes a DataFrame containing 'Application Property',
        geocodes each unique property, and returns a new DataFrame
        with columns:
            - property_cleaned_address
            - property_latitude
            - property_longitude
            - property_full_location_name
        merged in.

        No caching to disk. No file I/O.
        """

    if "Application Property" not in df.columns:
        raise ValueError("Dataframe must contain 'Application Property' column.")

    props = (
        df["Application Property"]
        .dropna()
        .astype(str)
        .drop_duplicates()
    )

    geolocator = Nominatim(user_agent="property_geo", timeout=20)
    rows = []

    for i, prop in enumerate(props, start=1):
        street, city = split_property(prop)
        cleaned_addr = ", ".join([p for p in (street, city) if p]).strip(", ")
        queries = build_query_variants(street, city)

        lat = lon = full_addr = None

        for q in queries:
            try:
                loc = geolocator.geocode(q)
                if loc:
                    lat, lon, full_addr = loc.latitude, loc.longitude, loc.address
                    break
            except Exception:
                pass

            time.sleep(1.2)  # Nominatim politeness

        rows.append({
            "Application Property": prop,
            "property_cleaned_address": cleaned_addr,
            "property_latitude": lat,
            "property_longitude": lon,
            "property_full_location_name": full_addr,
        })

    geo_df = pd.DataFrame(rows)

    # Merge back into original df
    return df.merge(geo_df, on="Application Property", how="left")
