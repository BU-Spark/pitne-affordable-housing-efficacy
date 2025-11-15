from __future__ import annotations
# 07_find_chapa_properties.py
#
# Extract unique CHAPA properties from applications_clean.parquet
# and save them with applicant counts.

from pathlib import Path
import pandas as pd

# --- paths ---
BASE_DIR = Path(__file__).resolve().parents[1]   
DATA_DIR = BASE_DIR / "data"
PROCESSED = DATA_DIR / "processed"

APPS_FILE = PROCESSED / "applications_clean.parquet"
OUT_FILE = PROCESSED / "chapa_properties_from_apps.csv"


def main():
    if not APPS_FILE.exists():
        raise SystemExit(f"Missing input file: {APPS_FILE}")

    print(f"📄 Loading applications: {APPS_FILE}")
    df = pd.read_parquet(APPS_FILE)
    print(f"   rows = {len(df):,}, cols = {len(df.columns)}")

    if "Application Property" not in df.columns:
        raise SystemExit("Column 'Application Property' not found in applications_clean.parquet")

    # Group to get applicant counts per property
    props = (
        df.groupby("Application Property")
          .size()
          .reset_index(name="applicant_count")
          .sort_values("Application Property")
          .reset_index(drop=True)
    )

    PROCESSED.mkdir(parents=True, exist_ok=True)
    props.to_csv(OUT_FILE, index=False)

    print(f"\n🏠 Found {len(props)} unique CHAPA properties")
    print(f"💾 Saved to: {OUT_FILE}")
    print("\nPreview:")
    print(props.head())


if __name__ == "__main__":
    main()
