from __future__ import annotations
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 14:36:44 2025

@author: brend

EDITS:
    kristenbestavros - wrapped Brendan's work in a function so it can be called externally.
"""
from pathlib import Path
from geopy.geocoders import Nominatim
import time
import pandas as pd

# === ADDED: importable geocoder with caching + polite rate limiting ===
def geocode_ma_cities(cities, cache_path: str | Path = "data/cache/geocode.parquet"):
    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        cache = pd.read_parquet(cache_path)
    else:
        cache = pd.DataFrame(columns=["city","longitude","latitude","full_location_name"])

    known = set(cache["city"].astype(str))
    to_do = sorted(set(str(c) for c in cities if pd.notna(c)) - known)
    if not to_do:
        return cache

    geolocator = Nominatim(user_agent="chapa_ma_city_coords", timeout=10)
    new_rows = []
    for city in to_do:
        try:
            loc = geolocator.geocode(f"{city}, Massachusetts, USA")
            if loc:
                new_rows.append({
                    "city": city,
                    "longitude": loc.longitude,
                    "latitude":  loc.latitude,
                    "full_location_name": loc.address,
                })
            else:
                new_rows.append({"city": city, "longitude": None, "latitude": None, "full_location_name": None})
        except Exception:
            new_rows.append({"city": city, "longitude": None, "latitude": None, "full_location_name": None})
        time.sleep(1)  # be polite to Nominatim

    new_df = pd.DataFrame(new_rows)
    if cache.empty:
        out = new_df
    elif new_df.empty:
        out = cache
    else:
        out = pd.concat([cache, new_df], ignore_index=True)

    out = out.drop_duplicates("city", keep="last")
    out.to_parquet(cache_path, index=False)
    return out

