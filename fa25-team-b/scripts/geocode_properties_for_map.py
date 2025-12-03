#!/usr/bin/env python3
"""
Geocode all unique properties from applications data and save to cache.

This script uses the applicant_property_geocoding module to get actual
property coordinates (not applicant residence coordinates).

Output: data/cache/property_coordinates.parquet
"""

import pandas as pd
import sys
from pathlib import Path

# Add cleaners to path
sys.path.insert(0, str(Path(__file__).parent.parent / "cleaners"))
from applicant_property_geocoding import applicant_property_geocoding

def main():
    print("Loading applications data...")
    df = pd.read_parquet("data/processed/applications_clean.parquet")

    print(f"Found {len(df)} applications across {df['Application Property'].nunique()} unique properties")

    # Get just unique properties for geocoding
    unique_props = df[['Application Property']].drop_duplicates()
    print(f"\nGeocoding {len(unique_props)} unique properties...")
    print("This will take ~2-3 minutes due to API rate limits...")

    # Geocode properties
    geocoded = applicant_property_geocoding(unique_props)

    # Check success rate
    success = geocoded['property_latitude'].notna().sum()
    total = len(geocoded)
    print(f"\nGeocoding complete: {success}/{total} properties successfully geocoded ({success/total*100:.1f}%)")

    # Save to cache
    output_path = "data/cache/property_coordinates.parquet"
    geocoded.to_parquet(output_path, index=False)
    print(f"Saved to {output_path}")

    # Show sample
    print("\n=== Sample Results ===")
    print(geocoded[['Application Property', 'property_latitude', 'property_longitude']].head(10).to_string())

    # Show failed geocodes
    failed = geocoded[geocoded['property_latitude'].isna()]
    if len(failed) > 0:
        print(f"\n=== Failed Geocodes ({len(failed)}) ===")
        print(failed['Application Property'].tolist())

if __name__ == "__main__":
    main()
