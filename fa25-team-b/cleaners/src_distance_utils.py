"""
Distance formulas for geographical coordinate pairs.
"""

import math


def haversine(lat1, lon1, lat2, lon2):
    """
    Great-circle distance using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371.0  # Earth radius (km)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
