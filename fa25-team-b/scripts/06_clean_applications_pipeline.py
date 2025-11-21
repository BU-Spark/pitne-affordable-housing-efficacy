from __future__ import annotations
from pathlib import Path
import pandas as pd, yaml, re
from tools.schema import standardize_columns
from cleaners.current_residence_name_normalization_v1 import normalize_current_residence
from cleaners.geographic_encoding_ma_cities import geocode_ma_cities
from cleaners.race_naming_normalization import normalize_race
from cleaners.append_resale_data import append_resale_data
from cleaners.HUD_economic_data_import_cleaning import import_clean_append_HUD
from cleaners.applicant_property_geocoding import applicant_property_geocoding

import time
from tqdm.auto import tqdm
import json
import numpy as np

RAW = Path("data/raw")
INTERIM = Path("data/interim"); INTERIM.mkdir(parents=True, exist_ok=True)
PROCESSED = Path("data/processed"); PROCESSED.mkdir(parents=True, exist_ok=True)
CONFIG = Path("config/datasets.yaml")
CITY_INDEX = "assets/city_names_norm_ma.csv"

def _stage(msg):
    print(f"\n— {msg}")

class Timer:
    def __enter__(self):
        self.t = time.perf_counter(); return self
    def __exit__(self, *args):
        print(f"   ✅ done in {time.perf_counter() - self.t:0.2f}s")

def load_apps_from_config():
    cfg = yaml.safe_load(CONFIG.read_text())
    items = cfg.get("applications", [])
    frames = []
    for it in items:
        name = it["name"]
        ftype = it.get("type", "xlsx")
        path = RAW / (name.replace(" ", "_").replace("/", "-") + (".csv" if ftype=="google_sheet" else ""))
        if not path.exists():
            print(f"[warn] missing raw: {path}")
            continue
        if path.suffix.lower() == ".xlsx":
            frames.append(pd.read_excel(path))
        elif path.suffix.lower() == ".csv":
            frames.append(pd.read_csv(path))
    if not frames:
        raise SystemExit("No application files found.")
    return pd.concat(frames, ignore_index=True)

def coerce_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse any column with 'date' in its name to pandas datetime."""
    date_like = [c for c in df.columns if re.search(r'date', c, flags=re.I)]
    for c in date_like:
        df[c] = pd.to_datetime(df[c], errors='coerce')
    return df

def _looks_numeric(series: pd.Series, thresh: float = 0.8) -> bool:
    """Heuristic: if >= thresh of non-null values parse as numbers, treat as numeric."""
    s = pd.to_numeric(series, errors='coerce')
    nonnull = series.notna().sum()
    if nonnull == 0:
        return False
    frac = s.notna().sum() / nonnull
    return frac >= thresh

def coerce_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce numeric-like object columns (e.g., 'Age' with 'u/a') to floats, mapping junk -> NaN."""
    for c in df.columns:
        if df[c].dtype == 'object':
            # Skip obvious non-numeric fields by name if you like:
            if re.search(r'(name|address|city|race|type|id$)', c, flags=re.I):
                continue
            if _looks_numeric(df[c]):
                df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

def coerce_objects(df: pd.DataFrame) -> pd.DataFrame:
    """Make any remaining Python objects (lists/dicts) safe for Arrow by stringifying them."""
    for c in df.columns:
        if df[c].dtype == 'object':
            # If elements are lists/dicts/misc, stringify them
            if df[c].map(lambda x: isinstance(x, (list, dict)) or type(x).__name__ not in ('str','float','int','bool','NoneType')).any():
                df[c] = df[c].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else (None if pd.isna(x) else str(x)))
    return df

def sanitize_for_parquet(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dtypes so Arrow is happy: dates → datetime64, numeric-like → numbers, others left as string/object."""
    df = coerce_dates(df)
    df = coerce_numerics(df)
    df = coerce_objects(df)
    return df

def run():
    # load + standardize
    _stage("Loading applications from config and standardizing headers")
    with Timer():
        df = load_apps_from_config()
        df = standardize_columns(df)
        df.to_csv(INTERIM / "df_cleaning_v1.csv", index=False)

    # residence normalization
    _stage("Normalizing current residence (fuzzy match to MA cities)")
    with Timer():
        df = normalize_current_residence(df, CITY_INDEX)

    # geocoding
    if "matched_city" in df.columns:
        unique_cities = df["matched_city"].dropna().astype(str).unique().tolist()
        print(f"   {len(unique_cities)} unique cities to check (cached cities are skipped).")
        _stage("Geocoding matched cities")
        with Timer():
            geo = geocode_ma_cities(unique_cities, cache_path="data/cache/geocode.parquet")
            df = df.merge(geo, left_on="matched_city", right_on="city", how="left")
            if "city" in df.columns:
                df.drop(columns=["city"], inplace=True)

    # race normalization
    _stage("Normalizing race")
    with Timer():
        target_race_col = "Race/Ethnicity" if "Race/Ethnicity" in df.columns else df.columns[df.columns.str.contains("race", case=False)][0]
        df = normalize_race(df, col=target_race_col)

    # append resale data
    _stage("Appending resale price data")
    with Timer():
        df = append_resale_data(df)

    # append MTSP Income Limit data
    _stage("Appending Applicant MTSP Income Limit data")
    with Timer():
        df = import_clean_append_HUD(df)

        _stage("Appending Property Geocoding")
    with Timer():
        df = applicant_property_geocoding(df)

    # remove redundant residence columns in final output
    cols_to_drop = [
        "Current Residence",
        "current_residence_norm_v1",
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    # ensure parquet-safe dtypes
    df = sanitize_for_parquet(df)

    # write output
    _stage("Writing cleaned applications parquet")
    with Timer():
        out = PROCESSED / "applications_clean.parquet"
        df.to_parquet(out, index=False)
        print("   →", out)

# allow import from 05_clean_pipeline
_run_apps = run


if __name__ == "__main__":
    run()