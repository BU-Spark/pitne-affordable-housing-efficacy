"""
Compute great-circle distances between applicant origins and property destinations
using Google Geocoding API.

Input file name:
    cleaned_c_residence_county_matched.csv

Output file:
    data/with_distance.csv
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path
from geocode_utils import load_gmaps, geocode_with_cache
from distance_utils import haversine


# ========== 1. CONFIG ==========
API_KEY = "AIzaSyCVn8dnvIDTfEAP3v7H-rdfvoc7a2My4o4"

INPUT_FILE = Path("data/cleaned_c_residence_county_matched.csv")
OUTPUT_FILE = Path("data/with_distance.csv")

# ========== 2. LOAD DATA ==========
print("Loading input data...")
df = pd.read_csv(INPUT_FILE)

required_cols = [
    "Current Residence Town",
    "Current Residence State",
    "Application Property Street Address",
    "Unit Number",
    "Application Property Town",
]

for c in required_cols:
    if c not in df.columns:
        raise ValueError(f"Missing column: {c}")

# ========== 3. BUILD ADDRESS STRINGS ==========
df["origin_addr"] = (
    df["Current Residence Town"].astype(str).str.strip()
    + ", "
    + df["Current Residence State"].astype(str).str.strip()
)

def build_destination(row):
    street = str(row["Application Property Street Address"]).strip()
    unit = row["Unit Number"]
    unit = "" if pd.isna(unit) else str(unit).strip()
    town = str(row["Application Property Town"]).strip()

    if unit:
        return f"{street}, {unit}, {town}, MA"
    else:
        return f"{street}, {town}, MA"

df["dest_addr"] = df.apply(build_destination, axis=1)

# ========== 4. INIT GEOCODER + CACHE ==========
gmaps = load_gmaps(API_KEY)
cache = {}

# ========== 5. GEOCODE + DISTANCE COMPUTATION ==========
origin_lat, origin_lng = [], []
dest_lat, dest_lng = [], []
dist_km, dist_mi = [], []

print("Computing geocodes and distances...")

for i, row in df.iterrows():
    o_addr = row["origin_addr"]
    d_addr = row["dest_addr"]

    o_lat, o_lng = geocode_with_cache(gmaps, o_addr, cache)
    d_lat, d_lng = geocode_with_cache(gmaps, d_addr, cache)

    origin_lat.append(o_lat)
    origin_lng.append(o_lng)
    dest_lat.append(d_lat)
    dest_lng.append(d_lng)

    if None in (o_lat, o_lng, d_lat, d_lng):
        dist_km.append(None)
        dist_mi.append(None)
    else:
        d_km = haversine(o_lat, o_lng, d_lat, d_lng)
        dist_km.append(d_km)
        dist_mi.append(d_km * 0.621371)

df["origin_lat"] = origin_lat
df["origin_lng"] = origin_lng
df["dest_lat"] = dest_lat
df["dest_lng"] = dest_lng
df["distance_km"] = dist_km
df["distance_miles"] = dist_mi

# ========== 6. SAVE ==========
print(f"Saving output → {OUTPUT_FILE}")
df.to_csv(OUTPUT_FILE, index=False)
print("Done.")
