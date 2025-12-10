"""
Utility functions for geocoding using the Google Geocoding API.

Features:
- Address normalization
- Caching to avoid duplicate API calls
- Safe error handling
"""

from __future__ import annotations
import pandas as pd
import googlemaps
from pathlib import Path
from typing import Tuple, Optional
from time import sleep


def load_gmaps(api_key: str) -> googlemaps.Client:
    """Initialize Google Maps geocoder client."""
    return googlemaps.Client(key=api_key)


def geocode_with_cache(
    gmaps_client,
    address: str,
    cache: dict,
    sleep_sec: float = 0.1
) -> Tuple[Optional[float], Optional[float]]:
    """
    Geocode an address with in-memory cache to avoid repeated API calls.
    Returns (lat, lng).
    """

    if address in cache:
        return cache[address]

    try:
        res = gmaps_client.geocode(address)
        if not res:
            cache[address] = (None, None)
        else:
            loc = res[0]["geometry"]["location"]
            cache[address] = (loc["lat"], loc["lng"])
    except Exception as e:
        print(f"[WARN] Geocode failed for: {address} | {e}")
        cache[address] = (None, None)

    sleep(sleep_sec)  # avoid hitting rate limits
    return cache[address]
