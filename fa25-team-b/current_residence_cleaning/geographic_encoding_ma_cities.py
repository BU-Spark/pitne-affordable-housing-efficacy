# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 14:36:44 2025

@author: brend
"""

import pandas as pd

apps = pd.read_csv('df_cleaning.csv')
cities_ma_file = pd.read_csv('city_names_norm_ma.csv')

cities_ma = cities_ma_file['city_manchester_manually_adjusted']
cities_ma = cities_ma.rename(columns={'city_manchester_manually_adjusted':'mass_cities_norm'})

# cities_ma = cities_ma.tolist()

#%% geocoding MA city list

import numpy as np
import math
from geopy.geocoders import Nominatim


def geocode_ma_cities(cities_ma):
    geolocator = Nominatim(user_agent='ma_city_coords', timeout=5)
    
    rows = []
    for city in cities_ma:
        full_location = geolocator.geocode(f'{city}, Massachusetts, USA')
        rows.append({
            'city': city,
            'longitude': full_location.longitude,
            'latitude': full_location.latitude,
            'full_location_name': full_location.address
        })
    return pd.DataFrame(rows)

cities_geo_encoded = geocode_ma_cities(cities_ma)

# print(cities_geo_encoded.head(5)) # check function ran properly
