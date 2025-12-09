#!/usr/bin/env python3
"""
Enhanced Interactive Folium Map Generator for Property Popularity Analysis

Features:
- Property markers with demographic pie charts
- Directional flow lines showing applicant origins
- Multiple heatmap layers (applicant origins, price)
- Massachusetts town choropleth with demographics
- Interactive search and filtering
- Age and demographic data in popups
"""

from __future__ import annotations
import argparse
import logging
import os
import json
import re
import requests
from typing import Tuple
from collections import defaultdict

import folium
from folium.plugins import MarkerCluster, HeatMap, MiniMap, Fullscreen, MeasureControl, LocateControl, Search
from folium import FeatureGroup, LayerControl, DivIcon, PolyLine, Marker, CircleMarker, Choropleth, GeoJson
import branca.colormap as cm
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")

# Config
DEFAULT_OUTPUT = "visuals"
PROP_COL = "Application Property"
PRICE_COL = "Property Maximum Resale Price"
PROP_LON_COL = "property_longitude"
PROP_LAT_COL = "property_latitude"
APPLICANT_LON_COL = "longitude"
APPLICANT_LAT_COL = "latitude"

DEMO_COLS = {
    "dummy_asian": ("Asian", "#F59E0B"),
    "dummy_black_african_american": ("Black/African American", "#0F766E"),
    "dummy_hispanic": ("Hispanic/Latine", "#7C3AED"),
    "dummy_white": ("White", "#2563EB"),
    "dummy_native_american_alaskan_native": ("Native American/Alaskan Native", "#DC2626"),
    "dummy_white_MENA": ("White (MENA)", "#0891B2"),
    "dummy_choose_not_to_answer": ("Prefer not to say", "#6B7280"),
    "dummy_unknown": ("Unknown", "#94A3B8"),
}

# Utility functions
def read_any(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file extension for {path}")

def load_bedroom_data() -> dict:
    """Load bedroom data from resale transaction info files and return property -> bedrooms mapping"""
    bedroom_data = {}

    # Try to load from various resale transaction info files
    resale_files = [
        "data/raw/Resale_Transaction_Info_-_Updated.xlsx",
        "data/raw/Resale_Transaction_Info_-_Confidential_updated_Sept_2025.xlsx",
        "data/raw/Resale_Transaction_Info_-_Confidential_(Google_Sheet).csv"
    ]

    for file_path in resale_files:
        if not os.path.exists(file_path):
            continue

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                # For Excel files, try different sheets
                xl = pd.ExcelFile(file_path)
                # Prefer processed sheets like 'final_round2' or first sheet
                sheet_name = 'final_round2' if 'final_round2' in xl.sheet_names else xl.sheet_names[0]
                df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Check if Bedrooms column exists
            if 'Bedrooms' not in df.columns:
                continue

            # Match based on Address and City columns (not Development)
            if 'Address' in df.columns and 'City' in df.columns:
                for _, row in df.iterrows():
                    if pd.notna(row.get('Bedrooms')) and pd.notna(row.get('Address')) and pd.notna(row.get('City')):
                        address = str(row['Address']).strip()
                        city = str(row['City']).strip()
                        bedrooms = int(row['Bedrooms'])

                        # Normalize the address for matching
                        # Remove common variations like "Street" -> "St", etc.
                        address_normalized = address.lower()
                        # Normalize all street types consistently
                        address_normalized = address_normalized.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
                        address_normalized = address_normalized.replace(' drive', ' dr').replace(' lane', ' ln')
                        # Also handle st., rd., ave., dr. with periods
                        address_normalized = address_normalized.replace(' st.', ' st').replace(' rd.', ' rd').replace(' ave.', ' ave')
                        address_normalized = address_normalized.replace(' dr.', ' dr').replace(' ln.', ' ln')
                        # Remove trailing periods and commas
                        address_normalized = address_normalized.rstrip(',.').strip()

                        city_normalized = city.lower()

                        # Create keys that match Application Property format patterns
                        # Application Property formats seen:
                        #   "1 Millbrook Lane Unit 213 ~ Wakefield"
                        #   "13 Coppersmith Way ~ Townsend"
                        #   "501 Commerce Drive Unit 1-116 ~ Braintree"

                        # Store with normalized key: "address ~ city"
                        key = f"{address_normalized} ~ {city_normalized}"
                        if key not in bedroom_data:
                            bedroom_data[key] = []
                        bedroom_data[key].append(bedrooms)

            logging.info(f"Loaded bedroom data from {file_path}: {len(bedroom_data)} unique address-city pairs")
        except Exception as e:
            logging.warning(f"Could not load bedroom data from {file_path}: {e}")
            continue

    # Convert lists to mode (most common bedroom count)
    from scipy import stats
    bedroom_map = {}
    for prop_key, bedrooms_list in bedroom_data.items():
        if bedrooms_list:
            # Use mode, or if tie, use the smaller number
            mode_result = stats.mode(bedrooms_list, keepdims=True)
            bedroom_map[prop_key] = int(mode_result.mode[0])

    logging.info(f"Created bedroom mapping for {len(bedroom_map)} properties")
    return bedroom_map

def normalize_property_for_bedroom_match(property_str: str) -> str:
    """
    Normalize an Application Property string to match bedroom_map keys.

    Examples:
        "1 Millbrook Lane Unit 213 ~ Wakefield" -> "1 millbrook lane ~ wakefield"
        "13 Coppersmith Way ~ Townsend" -> "13 coppersmith way ~ townsend"
        "501 Commerce Drive Unit 1-116 ~ Braintree" -> "501 commerce drive ~ braintree"
    """
    if pd.isna(property_str):
        return None

    prop_str = str(property_str).lower().strip()
    import re

    # Handle different formats
    # Format 1: "Address Unit X ~ City" or "Address ~City" (no space after ~)
    # Format 2: "City, Address"
    # Format 3: "City - Address"

    # First, fix cases where there's no space after ~
    prop_str = re.sub(r'~(?!\s)', '~ ', prop_str)

    if ' ~ ' in prop_str:
        # Split on ~ to get address and city
        parts = prop_str.split(' ~ ')
        if len(parts) == 2:
            address_part = parts[0].strip()
            city_part = parts[1].strip()

            # Remove unit numbers from address (e.g., "Unit 213", "Unit 1-116", "#117", "F2,")
            # Be careful not to remove the entire address if it starts with "Unit"
            address_part = re.sub(r',?\s+unit\s+#?\s*[\w\-]+', '', address_part, flags=re.IGNORECASE)
            address_part = re.sub(r',?\s*#\s*[\w\-]+', '', address_part)
            address_part = re.sub(r',\s*[a-z]\d+,?', '', address_part, flags=re.IGNORECASE)  # Remove unit codes like F2, A1

            # Remove "Unit X" if it comes after a comma
            address_part = re.sub(r',\s+unit\s+[\w\-]+$', '', address_part, flags=re.IGNORECASE)

            # Normalize street types
            address_part = address_part.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
            address_part = address_part.replace(' drive', ' dr').replace(' lane', ' ln')
            # Also handle st., rd., ave., dr. with periods
            address_part = address_part.replace(' st.', ' st').replace(' rd.', ' rd').replace(' ave.', ' ave')
            address_part = address_part.replace(' dr.', ' dr').replace(' ln.', ' ln')

            # Remove any trailing commas, periods, or spaces
            address_part = address_part.rstrip(',.').strip()

            # Clean city part (remove age restrictions, notes)
            city_part = re.sub(r'\s*\(.*?\)', '', city_part).strip()
            # Remove prefixes like "East", "West", "North", "South" for better matching
            # Actually, keep them as they might be important - but normalize "East Taunton" issue separately

            return f"{address_part} ~ {city_part}"

    elif ', ' in prop_str:
        # Format: "City, Address" OR "Address, Unit X"
        # Need to distinguish between these two cases
        parts = prop_str.split(', ')

        # If first part looks like an address (starts with a number), treat differently
        if len(parts) >= 2:
            if re.match(r'^\d', parts[0]):
                # Likely "Address, Unit X" format - keep first part as address, ignore unit
                address_part = parts[0].strip()
                # Try to extract city from somewhere else? For now, return None
                # Normalize street types
                address_part = address_part.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
                # Can't determine city, so this won't match - return None
                return None
            else:
                # Likely "City, Address" format
                city_part = parts[0].strip()
                address_part = parts[1].strip()

                # Remove unit numbers from address
                address_part = re.sub(r'\s+unit\s+[\w\-]+', '', address_part, flags=re.IGNORECASE)

                # Normalize street types
                address_part = address_part.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
                address_part = address_part.replace(' drive', ' dr').replace(' lane', ' ln')
                address_part = address_part.rstrip(',.').strip()

                return f"{address_part} ~ {city_part}"

    elif ' - ' in prop_str:
        # Format: "City - Address" - swap to "Address ~ City"
        parts = prop_str.split(' - ', 1)
        if len(parts) == 2:
            city_part = parts[0].strip()
            address_part = parts[1].strip()

            # Remove unit numbers
            address_part = re.sub(r'\s+unit\s+[\w\-]+', '', address_part, flags=re.IGNORECASE)
            address_part = re.sub(r'\s*#\s*[\w\-]+', '', address_part)

            # Normalize street types
            address_part = address_part.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
            address_part = address_part.replace(' drive', ' dr').replace(' lane', ' ln')
            address_part = address_part.rstrip(',.').strip()

            # Clean city part
            city_part = re.sub(r'\s*\(.*?\)', '', city_part).strip()

            return f"{address_part} ~ {city_part}"

    return None

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def to_float_series(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")

def haversine_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * 3956  # miles

def download_ma_geojson(cache_path: str = "data/cache/ma_towns.geojson") -> str:
    """Download Massachusetts town boundaries GeoJSON"""
    if os.path.exists(cache_path):
        logging.info(f"Using cached MA boundaries: {cache_path}")
        return cache_path

    logging.info("Downloading Massachusetts town boundaries...")

    # Use MassGIS data source for MA towns
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/massachusetts-towns.geojson"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            ensure_dir(os.path.dirname(cache_path))
            with open(cache_path, 'w') as f:
                json.dump(data, f)
            logging.info(f"Downloaded and cached MA boundaries to {cache_path}")
            return cache_path
    except Exception as e:
        logging.warning(f"Could not download GeoJSON: {e}")
        logging.warning("Creating empty placeholder")

    # Create empty placeholder
    ma_geojson = {"type": "FeatureCollection", "features": []}
    ensure_dir(os.path.dirname(cache_path))
    with open(cache_path, 'w') as f:
        json.dump(ma_geojson, f)

    return cache_path

def create_pie_chart_marker_html(row, demo_cols_dict, property_id):
    """Create HTML for pie chart marker with unique ID for highlighting. Returns (html, size)."""
    demo_values = []
    demo_colors = []

    for col, (label, color) in demo_cols_dict.items():
        if col in row.index and pd.notna(row[col]) and row[col] > 0:
            demo_values.append(row[col])
            demo_colors.append(color)

    if not demo_values:
        return None, None

    total = sum(demo_values)
    if total == 0:
        return None, None

    percentages = [v / total * 100 for v in demo_values]

    # Scale size
    app_count = int(row.get('application_count', 20))
    base_size = 25
    size = int(base_size + np.sqrt(app_count) * 3)
    size = min(size, 80)

    # Build conic-gradient
    gradient_stops = []
    cumulative = 0
    for pct, color in zip(percentages, demo_colors):
        start = cumulative
        cumulative += pct
        gradient_stops.append(f"{color} {start}% {cumulative}%")

    gradient = f"conic-gradient({', '.join(gradient_stops)})"

    html = f"""
    <div class="pie-marker" data-property-id="{property_id}" style="
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        background: {gradient};
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    " onmouseover="this.style.transform='scale(1.2)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.6)';"
       onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.4)';"
       onclick="highlightFlows('{property_id}')"></div>
    """

    return html, size

def build_property_tables(df: pd.DataFrame, bedroom_map: dict = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Build property-level demand and attributes tables with age and bedroom data"""
    if PROP_COL not in df.columns:
        raise KeyError(f"Missing required column: {PROP_COL}")

    if PROP_LAT_COL not in df.columns or PROP_LON_COL not in df.columns:
        raise KeyError("Property coordinates not found. Run cleaning pipeline.")

    demand = (
        df.groupby(PROP_COL).size()
          .reset_index(name="application_count")
          .rename(columns={PROP_COL: "Property"})
          .sort_values("application_count", ascending=False)
    )

    # Add bedroom data if available
    if bedroom_map:
        # Normalize property names and match against bedroom_map
        demand['property_normalized'] = demand['Property'].apply(normalize_property_for_bedroom_match)
        demand['bedrooms'] = demand['property_normalized'].map(bedroom_map)
        demand.drop(columns=['property_normalized'], inplace=True)

    price_num = to_float_series(df[PRICE_COL]) if PRICE_COL in df.columns else pd.Series([np.nan]*len(df))
    applicant_lon = to_float_series(df[APPLICANT_LON_COL]) if APPLICANT_LON_COL in df.columns else pd.Series([np.nan]*len(df))
    applicant_lat = to_float_series(df[APPLICANT_LAT_COL]) if APPLICANT_LAT_COL in df.columns else pd.Series([np.nan]*len(df))
    prop_lon = to_float_series(df[PROP_LON_COL])
    prop_lat = to_float_series(df[PROP_LAT_COL])

    # Extract age data if available
    age_col = None
    for possible_age_col in ["Age", "age", "Applicant Age", "applicant_age"]:
        if possible_age_col in df.columns:
            age_col = possible_age_col
            break

    age_data = to_float_series(df[age_col]) if age_col else pd.Series([np.nan]*len(df))

    agg_dict = {
        "price_num": ("price_num", "median"),
        "applicant_median_lon": ("applicant_median_lon", "median"),
        "applicant_median_lat": ("applicant_median_lat", "median"),
        "property_longitude": (PROP_LON_COL, "first"),
        "property_latitude": (PROP_LAT_COL, "first"),
    }

    # Add age aggregations if age data exists
    if age_col:
        agg_dict["median_age"] = ("age_data", "median")
        agg_dict["mean_age"] = ("age_data", "mean")
        agg_dict["min_age"] = ("age_data", "min")
        agg_dict["max_age"] = ("age_data", "max")

    attrs = (
        pd.DataFrame({
            PROP_COL: df[PROP_COL],
            "price_num": price_num,
            "applicant_median_lon": applicant_lon,
            "applicant_median_lat": applicant_lat,
            PROP_LON_COL: prop_lon,
            PROP_LAT_COL: prop_lat,
            "age_data": age_data,
        })
        .groupby(PROP_COL, as_index=False)
        .agg(**agg_dict)
        .rename(columns={PROP_COL: "Property"})
    )

    # Calculate distances
    distances = []
    for _, row in df.iterrows():
        if pd.notna(row[PROP_LAT_COL]) and pd.notna(row[PROP_LON_COL]) and \
           pd.notna(row[APPLICANT_LAT_COL]) and pd.notna(row[APPLICANT_LON_COL]):
            dist = haversine_distance(
                row[APPLICANT_LAT_COL], row[APPLICANT_LON_COL],
                row[PROP_LAT_COL], row[PROP_LON_COL]
            )
            distances.append({"Property": row[PROP_COL], "distance_miles": dist})

    if distances:
        dist_df = pd.DataFrame(distances)
        median_dist = dist_df.groupby("Property")["distance_miles"].agg(
            median_distance_miles="median",
            avg_distance_miles="mean",
            min_distance_miles="min",
            max_distance_miles="max"
        ).reset_index()
        attrs = attrs.merge(median_dist, on="Property", how="left")
    else:
        for col in ["median_distance_miles", "avg_distance_miles", "min_distance_miles", "max_distance_miles"]:
            attrs[col] = np.nan

    return demand, attrs

def plot_v4_enhanced_map(demand: pd.DataFrame, df: pd.DataFrame, outdir: str) -> None:
    """Create enhanced interactive map with all requested features"""
    try:
        geo = demand.dropna(subset=[PROP_LAT_COL, PROP_LON_COL]).copy()
        if geo.empty:
            logging.warning("Map skipped: no valid property coordinates.")
            return

        logging.info(f"Creating enhanced map for {len(geo)} properties...")

        # Aggregate demographics and age to property level
        demo_cols_present = [c for c in DEMO_COLS.keys() if c in df.columns]
        if demo_cols_present:
            demo_shares = (
                df.groupby(PROP_COL)[demo_cols_present].mean()
                  .reset_index()
                  .rename(columns={PROP_COL: "Property"})
            )
            geo = geo.merge(demo_shares, on="Property", how="left")

        # Base map
        center = [geo[PROP_LAT_COL].median(), geo[PROP_LON_COL].median()]
        m = folium.Map(location=center, zoom_start=8, tiles="CartoDB positron")

        # Property ID mapping for highlighting
        prop_id_to_idx = {f"prop_{idx}": idx for idx in geo.index}
        prop_to_town = {}
        if "property_city" in df.columns or "Property City" in df.columns:
            city_col = "property_city" if "property_city" in df.columns else "Property City"
            prop_city_map = df.groupby(PROP_COL)[city_col].first().to_dict()
            for prop in geo['Property']:
                prop_to_town[prop] = prop_city_map.get(prop, "")

        # PIE CHART MARKERS with age and demographic data
        logging.info("Creating pie chart markers with detailed popups...")
        pie_layer = FeatureGroup(name="Properties (Pie Charts)", show=True)

        # Store property data for filtering
        properties_data = []

        for idx, row in geo.iterrows():
            # Use property name as unique identifier to ensure consistency with flow mapping
            # Sanitize property name: only allow alphanumeric, underscore, hyphen (CSS-safe)
            sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', row['Property'])
            property_id = f"prop_{sanitized_name}"
            pie_html, marker_size = create_pie_chart_marker_html(row, DEMO_COLS, property_id)

            if pie_html and marker_size:
                # Create detailed popup with race and age info
                price_txt = f"${row['price_num']:,.0f}" if pd.notna(row.get("price_num")) else "—"
                dist_median = f"{row['median_distance_miles']:.1f} mi" if pd.notna(row.get("median_distance_miles")) else "—"
                dist_avg = f"{row['avg_distance_miles']:.1f} mi" if pd.notna(row.get("avg_distance_miles")) else "—"
                dist_range = f"{row['min_distance_miles']:.1f}–{row['max_distance_miles']:.1f} mi" if pd.notna(row.get("min_distance_miles")) else "—"

                # Age data
                median_age_txt = f"{row['median_age']:.1f} years" if pd.notna(row.get("median_age")) else "—"
                mean_age_txt = f"{row['mean_age']:.1f} years" if pd.notna(row.get("mean_age")) else "—"
                age_range_txt = f"{row['min_age']:.0f}–{row['max_age']:.0f} years" if pd.notna(row.get("min_age")) else "—"

                def pct(x):
                    return f"{x*100:.0f}%" if pd.notna(x) else "—"

                # Demographics horizontal bar items
                demo_items = []
                for key, (label, color) in DEMO_COLS.items():
                    if key in row.index and pd.notna(row[key]) and row[key] > 0:
                        percentage = row[key] * 100
                        demo_items.append(f"""
                            <div style='margin: 4px 0;'>
                                <div style='font-size:10px; color:#475569; margin-bottom:2px;'>{label}</div>
                                <div style='position:relative; background:#E2E8F0; height:20px; border-radius:3px; overflow:hidden;'>
                                    <div style='background:{color}; height:100%; width:{percentage:.1f}%; transition: width 0.3s;'></div>
                                    <div style='position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:11px; font-weight:600; color:#0F172A; text-shadow: 0 0 3px white, 0 0 3px white;'>{percentage:.0f}%</div>
                                </div>
                            </div>
                        """)

                demo_content = "".join(demo_items) if demo_items else "<div style='font-style:italic; color:#64748B; font-size:11px;'>No demographic data</div>"

                # Bedroom data
                bedrooms_txt = f"{int(row['bedrooms'])} BR" if pd.notna(row.get("bedrooms")) else "—"

                popup_content = f"""
                <div style="font-family: system-ui, Arial; font-size: 12px; line-height:1.4; min-width:550px; max-width:650px;">
                    <div style="font-size: 15px; font-weight:600; margin-bottom:10px; color:#0F172A; border-bottom: 2px solid #0F766E; padding-bottom:6px;">
                        {row['Property']}
                    </div>

                    <!-- Property Info Grid -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom:12px;">
                        <!-- Left Column -->
                        <div style="background: #F8FAFC; padding: 10px; border-radius: 6px; border-left: 3px solid #0F766E;">
                            <div style="font-weight:600; font-size:11px; color:#64748B; margin-bottom:8px; text-transform: uppercase;">Property Details</div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0;">
                                <span style="color:#475569;">Applications:</span>
                                <b style="color:#0F766E; font-size:13px;">{int(row['application_count'])}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0;">
                                <span style="color:#475569;">Bedrooms:</span>
                                <b style="color:#1E40AF;">{bedrooms_txt}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0;">
                                <span style="color:#475569;">Max Resale Price:</span>
                                <b>{price_txt}</b>
                            </div>
                        </div>

                        <!-- Right Column -->
                        <div style="background: #F8FAFC; padding: 10px; border-radius: 6px; border-left: 3px solid #3B82F6;">
                            <div style="font-weight:600; font-size:11px; color:#64748B; margin-bottom:8px; text-transform: uppercase;">Applicant Stats</div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0; font-size:11px;">
                                <span style="color:#475569;">Median Age:</span>
                                <b>{median_age_txt}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0; font-size:11px;">
                                <span style="color:#475569;">Age Range:</span>
                                <b>{age_range_txt}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0; font-size:11px;">
                                <span style="color:#475569;">Median Distance:</span>
                                <b>{dist_median}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin:4px 0; font-size:11px;">
                                <span style="color:#475569;">Distance Range:</span>
                                <b>{dist_range}</b>
                            </div>
                        </div>
                    </div>

                    <!-- Demographics Section -->
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 6px; border-left: 3px solid #7C3AED;">
                        <div style="font-weight:600; font-size:11px; color:#64748B; margin-bottom:8px; text-transform: uppercase;">Applicant Demographics</div>
                        {demo_content}
                    </div>
                </div>
                """

                # Center the marker icon on the property location
                icon_anchor = (marker_size // 2, marker_size // 2)

                marker = folium.Marker(
                    location=[row[PROP_LAT_COL], row[PROP_LON_COL]],
                    icon=DivIcon(html=pie_html, icon_anchor=icon_anchor),
                    popup=folium.Popup(
                        popup_content,
                        max_width=700,
                        showarrow=False,
                        offset=(330, 300)  # Position popup to the right side and vertically centered
                    ),
                    tooltip=f"{row['Property']} ({int(row['application_count'])} apps)"
                )
                marker.add_to(pie_layer)

                # Store for filtering
                properties_data.append({
                    'id': property_id,
                    'lat': float(row[PROP_LAT_COL]),
                    'lon': float(row[PROP_LON_COL]),
                    'name': str(row['Property']),
                    'apps': int(row['application_count']),
                    'price': float(row['price_num']) if pd.notna(row.get('price_num')) else None,
                    'dist': float(row['median_distance_miles']) if pd.notna(row.get('median_distance_miles')) else None,
                    'age': float(row['median_age']) if pd.notna(row.get('median_age')) else None,
                })

        pie_layer.add_to(m)

        # FLOW LINES - Straight, thick, opaque with direction indicators and demographic breakdown
        logging.info("Creating directional flow lines...")
        if APPLICANT_LAT_COL in df.columns and APPLICANT_LON_COL in df.columns:
            flow_layer = FeatureGroup(name="Applicant Flow Lines", show=False)  # Make visible by default so DOM elements exist

            # Determine age column
            age_col = None
            for possible_age_col in ["Age", "age", "Applicant Age", "applicant_age"]:
                if possible_age_col in df.columns:
                    age_col = possible_age_col
                    break

            # Get property cities for filtering
            prop_city_col = None
            app_city_col = "matched_city"
            if "property_city" in df.columns:
                prop_city_col = "property_city"
            elif "Property City" in df.columns:
                prop_city_col = "Property City"

            # Group by origin, destination, and city
            flow_cols = [APPLICANT_LAT_COL, APPLICANT_LON_COL, PROP_COL, app_city_col]
            if prop_city_col:
                flow_cols.append(prop_city_col)

            # Add demographic and age columns for aggregation
            demo_flow_cols = [c for c in demo_cols_present if c in df.columns]
            age_flow_cols = [age_col] if age_col else []

            applicant_origins = df[flow_cols + demo_flow_cols + age_flow_cols].dropna(
                subset=[APPLICANT_LAT_COL, APPLICANT_LON_COL, PROP_COL]
            ).copy()

            # Filter out same-town flows if we have city data
            if prop_city_col:
                applicant_origins = applicant_origins[
                    applicant_origins[app_city_col] != applicant_origins[prop_city_col]
                ]

            # Group and aggregate
            group_cols = [APPLICANT_LAT_COL, APPLICANT_LON_COL, PROP_COL, app_city_col]

            # Always count flows first
            flow_counts = applicant_origins.groupby(group_cols).size().reset_index(name='flow_count')

            # Aggregate demographics separately from flow counts
            # First get demographic sums
            if demo_flow_cols:
                demo_agg_cols = [col for col in demo_flow_cols if col in applicant_origins.columns]
                if demo_agg_cols:
                    try:
                        # Sum up demographic columns for each flow
                        demo_sums = applicant_origins.groupby(group_cols)[demo_agg_cols].sum().reset_index()
                        # Merge with counts
                        flow_grouped = flow_counts.merge(demo_sums, on=group_cols, how='left')
                        logging.info(f"Successfully aggregated {len(demo_agg_cols)} demographic columns for flows")
                    except Exception as e:
                        logging.warning(f"Could not aggregate demographics for flows: {e}")
                        flow_grouped = flow_counts
                else:
                    flow_grouped = flow_counts
            else:
                flow_grouped = flow_counts

            # Add age aggregations if available
            if age_col and age_col in applicant_origins.columns:
                try:
                    age_agg = applicant_origins.groupby(group_cols)[age_col].agg(['mean', 'median', 'min', 'max']).reset_index()
                    age_agg.columns = group_cols + [f'{age_col}_mean', f'{age_col}_median', f'{age_col}_min', f'{age_col}_max']
                    flow_grouped = flow_grouped.merge(age_agg, on=group_cols, how='left')
                    logging.info(f"Successfully aggregated age data for flows")
                except Exception as e:
                    logging.warning(f"Could not aggregate age for flows: {e}")

            # Merge with property coordinates
            flow_grouped = flow_grouped.merge(
                geo[["Property", PROP_LAT_COL, PROP_LON_COL]].reset_index(),
                left_on=PROP_COL,
                right_on="Property",
                how="left"
            )

            # Store flow line info for JavaScript highlighting
            flow_lines_data = []
            property_flow_mapping = {}  # Map property_id to list of flow line indices
            flow_line_counter = 0  # Track actual number of lines added to DOM

            # Create all flow lines (no minimum threshold)
            for idx, flow in flow_grouped.iterrows():
                if pd.notna(flow[PROP_LAT_COL]) and pd.notna(flow[PROP_LON_COL]):
                    # Use property name as unique identifier (must match marker ID generation)
                    # Sanitize property name: only allow alphanumeric, underscore, hyphen (CSS-safe)
                    property_name = flow['Property']
                    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', property_name)
                    property_id = f"prop_{sanitized_name}"

                    # Straight line coordinates
                    line_coords = [
                        [flow[APPLICANT_LAT_COL], flow[APPLICANT_LON_COL]],
                        [flow[PROP_LAT_COL], flow[PROP_LON_COL]]
                    ]

                    # Create tooltip with demographic and age breakdown
                    tooltip_parts = [f"{flow[app_city_col]} → {flow['Property']}"]
                    tooltip_parts.append(f"Applicants: {int(flow['flow_count'])}")

                    # Add age data if available
                    if age_col:
                        age_mean_col = f"{age_col}_mean"
                        age_median_col = f"{age_col}_median"
                        age_min_col = f"{age_col}_min"
                        age_max_col = f"{age_col}_max"

                        if age_mean_col in flow.index and pd.notna(flow[age_mean_col]):
                            tooltip_parts.append(f"Age (avg): {flow[age_mean_col]:.1f}")
                        if age_median_col in flow.index and pd.notna(flow[age_median_col]):
                            tooltip_parts.append(f"Age (median): {flow[age_median_col]:.1f}")
                        if age_min_col in flow.index and pd.notna(flow[age_min_col]):
                            tooltip_parts.append(f"Age range: {flow[age_min_col]:.0f}-{flow[age_max_col]:.0f}")

                    # Add demographic breakdown
                    demo_found = False
                    for col in demo_flow_cols:
                        if col in flow.index and pd.notna(flow[col]) and flow[col] > 0:
                            if not demo_found:
                                tooltip_parts.append("Demographics:")
                                demo_found = True
                            label = DEMO_COLS[col][0]
                            # Use float value for accurate percentage calculation
                            value = flow[col]
                            count_display = round(value)
                            tooltip_parts.append(f"  {label}: {count_display}")

                    tooltip_text = "<br>".join(tooltip_parts)

                    # Create line - make thinner (2px) and more transparent for less obstruction
                    # Note: We'll add a unique class after checking distance filter
                    line = folium.PolyLine(
                        locations=line_coords,
                        color="#3B82F6",
                        weight=3,
                        opacity=0.3,  # Reduced for better contrast with highlighted flows
                        tooltip=tooltip_text,
                        popup=folium.Popup(tooltip_text.replace("<br>", "\n"), max_width=300)
                    )

                    # Store line reference with property ID for highlighting
                    line._property_id = property_id

                    # Only add flow line if distance is 10+ miles
                    origin_lat = flow[APPLICANT_LAT_COL]
                    origin_lon = flow[APPLICANT_LON_COL]
                    dest_lat = flow[PROP_LAT_COL]
                    dest_lon = flow[PROP_LON_COL]

                    distance_miles = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)

                    if distance_miles < 10:
                        continue  # Skip flows under 10 miles

                    # Add unique class name for identification
                    line.options['className'] = f'flow-line flow-{flow_line_counter} prop-{property_id}'

                    line.add_to(flow_layer)

                    # Track property-to-flow mapping using actual counter
                    if property_id not in property_flow_mapping:
                        property_flow_mapping[property_id] = []
                    property_flow_mapping[property_id].append(flow_line_counter)

                    # Store for JavaScript
                    flow_lines_data.append({
                        'property_id': property_id,
                        'flow_idx': flow_line_counter,  # Use counter instead of original idx
                        'start_lat': float(flow[APPLICANT_LAT_COL]),
                        'start_lon': float(flow[APPLICANT_LON_COL]),
                        'end_lat': float(flow[PROP_LAT_COL]),
                        'end_lon': float(flow[PROP_LON_COL])
                    })

                    flow_line_counter += 1  # Increment after adding

            flow_layer.add_to(m)
            logging.info(f"Added {flow_line_counter} directional flow lines")

        # APPLICANT ORIGIN CIRCLES (replacing fuzzy heatmap)
        logging.info("Creating applicant origin circles...")
        if APPLICANT_LAT_COL in df.columns and APPLICANT_LON_COL in df.columns:
            applicant_data = df[[APPLICANT_LAT_COL, APPLICANT_LON_COL]].dropna()
            if len(applicant_data) > 0:
                # Count applicants at each location for sizing
                location_counts = applicant_data.groupby([APPLICANT_LAT_COL, APPLICANT_LON_COL]).size().reset_index(name='count')

                origin_layer = FeatureGroup(name="Applicant Origins", show=False)

                for _, loc in location_counts.iterrows():
                    # Scale circle size based on count (sqrt for better visual scaling)
                    radius = min(3 + np.sqrt(loc['count']) * 2, 15)  # Min 3, max 15

                    folium.CircleMarker(
                        location=[loc[APPLICANT_LAT_COL], loc[APPLICANT_LON_COL]],
                        radius=radius,
                        color='#2563EB',  # Blue border
                        fill=True,
                        fillColor='#3B82F6',  # Blue fill
                        fillOpacity=0.6,
                        weight=2,
                        tooltip=f"{int(loc['count'])} applicant(s) from this location"
                    ).add_to(origin_layer)

                origin_layer.add_to(m)

        # PRICE HEATMAP with normalized scale
        logging.info("Creating price heatmap with normalized scale...")
        price_data_raw = []
        valid_prices = []
        for _, row in geo.iterrows():
            if pd.notna(row.get("price_num")) and row["price_num"] > 0:
                price_data_raw.append([row[PROP_LAT_COL], row[PROP_LON_COL], row["price_num"]])
                valid_prices.append(row["price_num"])

        if price_data_raw and len(valid_prices) > 0:
            # Normalize to 0-1 range based on min/max
            min_price = min(valid_prices)
            max_price = max(valid_prices)
            price_range = max_price - min_price if max_price > min_price else 1

            price_data = [
                [lat, lon, (price - min_price) / price_range * 100]  # Scale to 0-100 for better visibility
                for lat, lon, price in price_data_raw
            ]

            HeatMap(
                price_data,
                name="Price Heatmap",
                radius=22,
                blur=20,
                max_zoom=11,
                show=False,
                overlay=True,
                control=True,
                gradient={
                    0.0: '#0000FF',  # blue (low price)
                    0.2: '#00FFFF',  # cyan
                    0.4: '#00FF00',  # green
                    0.6: '#FFFF00',  # yellow
                    0.8: '#FF8000',  # orange
                    1.0: '#FF0000'   # red (high price)
                }
            ).add_to(m)

        # Choropleth removed per user request

        # Add controls
        folium.LayerControl(collapsed=False, position='topright').add_to(m)
        MiniMap(toggle_display=True, position='bottomleft').add_to(m)
        Fullscreen(position='topleft').add_to(m)
        MeasureControl(primary_length_unit='miles', position='topleft').add_to(m)
        LocateControl(auto_start=False, position='topleft').add_to(m)

        # Prepare flow mapping for JavaScript (handle case where flow layer wasn't created)
        flow_mapping_json = json.dumps(property_flow_mapping) if 'property_flow_mapping' in locals() else '{}'
        flow_data_json = json.dumps(flow_lines_data) if 'flow_lines_data' in locals() else '[]'

        # PIE CHART LEGEND + FILTER PANEL (compact and repositioned)
        custom_html = rf"""
        <style>
        .leaflet-control-layers {{
            max-height: 500px;
            overflow-y: auto;
        }}
        .leaflet-popup-content {{
            margin: 0 !important;
            padding: 0 !important;
        }}

        /* Pie Chart Legend - positioned left but offset from fullscreen button */
        #pie-legend {{
            position: fixed;
            top: 10px;
            left: 60px;  /* Moved right to avoid fullscreen button */
            background: white;
            border: 2px solid #334155;
            border-radius: 8px;
            padding: 10px;
            z-index: 999;
            font-family: system-ui;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 180px;
        }}

        #pie-legend h4 {{
            margin: 0 0 6px 0;
            font-size: 12px;
            font-weight: 600;
            color: #0F172A;
            border-bottom: 2px solid #0F766E;
            padding-bottom: 3px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            margin: 3px 0;
            font-size: 10px;
        }}

        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 5px;
            border: 1px solid #ccc;
            flex-shrink: 0;
        }}

        /* Filter Panel - compact and collapsible */
        #filter-toggle {{
            position: fixed;
            bottom: 60px;
            right: 10px;
            background: #0F766E;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            cursor: pointer;
            z-index: 999;
            font-weight: 600;
            font-size: 13px;
            font-family: system-ui;
        }}

        #filter-toggle:hover {{
            background: #0D5E57;
        }}

        #filter-panel {{
            position: fixed;
            bottom: 105px;
            right: 10px;
            background: white;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 999;
            font-family: system-ui;
            font-size: 12px;
            max-width: 220px;
            border: 2px solid #334155;
            display: none;
        }}

        #filter-panel.show {{
            display: block;
        }}

        #filter-panel h3 {{
            margin: 0 0 10px 0;
            font-size: 13px;
            font-weight: 600;
            color: #0F172A;
            border-bottom: 2px solid #0F766E;
            padding-bottom: 4px;
        }}

        .filter-group {{
            margin-bottom: 10px;
        }}

        .filter-group label {{
            display: block;
            font-weight: 500;
            margin-bottom: 3px;
            color: #334155;
            font-size: 11px;
        }}

        .filter-group input[type="range"] {{
            width: 100%;
            margin: 3px 0;
        }}

        .filter-values {{
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #64748B;
            margin-top: 2px;
        }}

        .filter-group button {{
            background: #0F766E;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            font-weight: 500;
            font-size: 11px;
            margin-top: 6px;
        }}

        .filter-group button:hover {{
            background: #0D5E57;
        }}

        /* Flow line highlighting */
        .flow-line {{
            transition: stroke 0.3s, stroke-width 0.3s;
        }}

        .flow-line.highlighted {{
            stroke: #EAB308 !important;
            stroke-width: 8px !important;
        }}
        </style>

        <!-- Pie Chart Legend -->
        <div id="pie-legend">
            <h4>Pie Chart Colors</h4>
        """

        for col, (label, color) in DEMO_COLS.items():
            custom_html += f"""
            <div class="legend-item">
                <div class="legend-color" style="background-color: {color};"></div>
                <span>{label}</span>
            </div>
            """

        custom_html += f"""
        </div>

        <!-- Filter Toggle Button -->
        <button id="filter-toggle" onclick="toggleFilters()">🔍 Filters</button>

        <!-- Filter Panel -->
        <div id="filter-panel">
            <h3>Filter Properties</h3>

            <div class="filter-group">
                <label>Applications (min)</label>
                <input type="range" id="filter-apps-min" min="0" max="100" value="0" step="1">
                <div class="filter-values">
                    <span id="apps-min-val">0</span>
                    <span>100+</span>
                </div>
            </div>

            <div class="filter-group">
                <label>Price (max $)</label>
                <input type="range" id="filter-price-max" min="0" max="500000" value="500000" step="10000">
                <div class="filter-values">
                    <span>$0</span>
                    <span id="price-max-val">$500K+</span>
                </div>
            </div>

            <div class="filter-group">
                <label>Distance (max mi)</label>
                <input type="range" id="filter-dist-max" min="0" max="100" value="100" step="5">
                <div class="filter-values">
                    <span>0</span>
                    <span id="dist-max-val">100+</span>
                </div>
            </div>

            <div class="filter-group">
                <label>Age (max years)</label>
                <input type="range" id="filter-age-max" min="18" max="100" value="100" step="1">
                <div class="filter-values">
                    <span>18</span>
                    <span id="age-max-val">100+</span>
                </div>
            </div>

            <div class="filter-group">
                <button onclick="applyFilters()">Apply</button>
                <button onclick="resetFilters()" style="background: #64748B; margin-top: 3px;">Reset</button>
            </div>
        </div>

        <script type="text/javascript">
        // Property data for filtering
        var properties = {json.dumps(properties_data)};
        var flowLinesData = {flow_data_json};
        var propertyFlowMapping = {flow_mapping_json};
        var markers = {{}};  // Will store marker elements
        var currentHighlightedProperty = null;
        var allPolylines = [];  // Store all flow line polylines

        // Initialize after map loads - use longer timeout to ensure all layers are rendered
        setTimeout(function() {{
            console.log('=== Starting flow line initialization ===');

            // Find all SVG paths in the entire document
            var allPaths = document.querySelectorAll('svg path');
            console.log('Total SVG paths found:', allPaths.length);

            // Filter for blue flow lines
            allPaths.forEach(function(path) {{
                var stroke = path.getAttribute('stroke');
                var strokeStyle = path.style.stroke;

                // Check both attribute and style, and handle both hex and rgb formats
                if ((stroke && (stroke === '#3B82F6' || stroke.toLowerCase() === '#3b82f6')) ||
                    (strokeStyle && (strokeStyle === 'rgb(59, 130, 246)' || strokeStyle === '#3B82F6' || strokeStyle === '#3b82f6'))) {{
                    allPolylines.push(path);
                }}
            }});

            console.log('Found ' + allPolylines.length + ' flow lines (blue paths)');
            console.log('Flow data count:', flowLinesData.length);
            console.log('Flow mapping loaded for ' + Object.keys(propertyFlowMapping).length + ' properties');
            console.log('Sample property IDs:', Object.keys(propertyFlowMapping).slice(0, 5));

            // Debug: log first few flow line details
            if (allPolylines.length > 0) {{
                console.log('First flow line stroke:', allPolylines[0].getAttribute('stroke'));
                console.log('First flow line style:', allPolylines[0].style.stroke);
            }}

            console.log('=== Flow line initialization complete ===');

            // Also initialize choropleth click handlers
            console.log('=== Setting up choropleth interactions ===');
            var pathElements = document.querySelectorAll('svg path');
            var choroplethPaths = [];

            pathElements.forEach(function(path) {{
                // Choropleth paths typically have fill and different styling
                var fill = path.getAttribute('fill');
                var fillOpacity = path.getAttribute('fill-opacity');

                if (fill && fill !== 'none' && fillOpacity) {{
                    choroplethPaths.push(path);
                }}
            }});

            console.log('Found', choroplethPaths.length, 'potential choropleth paths');
            console.log('=== Choropleth initialization complete ===');
        }}, 3000);  // Increased timeout to 3 seconds

        function toggleFilters() {{
            var panel = document.getElementById('filter-panel');
            panel.classList.toggle('show');
        }}

        function highlightFlows(propertyId) {{
            console.log('=== highlightFlows called ===');
            console.log('Property ID:', propertyId);

            // Toggle behavior: if clicking the same property, unhighlight and return
            if (currentHighlightedProperty === propertyId) {{
                console.log('Toggling off - same property clicked');
                resetAllFlows();
                currentHighlightedProperty = null;
                return;
            }}

            // Reset all flows first
            resetAllFlows();

            // Find all flow lines for this property by class name
            // Class format: 'flow-line flow-{{idx}} prop-{{propertyId}}'
            var selector = 'path.prop-' + propertyId;
            console.log('Looking for flows with selector:', selector);

            var flowPaths = document.querySelectorAll(selector);
            console.log('Found', flowPaths.length, 'flow paths for this property');

            if (flowPaths.length === 0) {{
                console.log('No flows found for property');
                return;
            }}

            // Highlight each flow line
            var highlighted = 0;
            flowPaths.forEach(function(path) {{
                // Verify it's a flow line (has blue stroke)
                var stroke = path.getAttribute('stroke');
                if (stroke === '#3B82F6' || stroke === '#EAB308') {{
                    path.setAttribute('stroke', '#EAB308');
                    path.setAttribute('stroke-width', '5');
                    path.setAttribute('stroke-opacity', '1.0');
                    path.setAttribute('opacity', '1.0');
                    path.style.stroke = '#EAB308';
                    path.style.strokeWidth = '5';
                    path.style.strokeOpacity = '1.0';
                    path.style.opacity = '1.0';

                    // Move to end to render on top
                    var parent = path.parentNode;
                    if (parent) parent.appendChild(path);

                    highlighted++;
                }}
            }});

            console.log('=== Highlighting complete ===');
            console.log('Successfully highlighted:', highlighted, 'flows');
            currentHighlightedProperty = propertyId;
        }}

        function resetAllFlows() {{
            // Use class-based selection for efficiency - target all flow-line paths
            var flowPaths = document.querySelectorAll('path.flow-line');
            console.log('Resetting', flowPaths.length, 'flow lines');

            flowPaths.forEach(function(path) {{
                path.setAttribute('stroke', '#3B82F6');
                path.setAttribute('stroke-width', '3');
                path.setAttribute('stroke-opacity', '0.3');
                path.setAttribute('opacity', '0.3');
                path.style.stroke = '#3B82F6';
                path.style.strokeWidth = '3';
                path.style.strokeOpacity = '0.3';
                path.style.opacity = '0.3';
            }});
        }}

        // Update filter value displays
        document.getElementById('filter-apps-min').addEventListener('input', function(e) {{
            document.getElementById('apps-min-val').textContent = e.target.value;
        }});

        document.getElementById('filter-price-max').addEventListener('input', function(e) {{
            var val = parseInt(e.target.value);
            document.getElementById('price-max-val').textContent =
                val >= 500000 ? '$500K+' : '$' + Math.floor(val/1000) + 'K';
        }});

        document.getElementById('filter-dist-max').addEventListener('input', function(e) {{
            var val = parseInt(e.target.value);
            document.getElementById('dist-max-val').textContent = val >= 100 ? '100+' : val;
        }});

        document.getElementById('filter-age-max').addEventListener('input', function(e) {{
            var val = parseInt(e.target.value);
            document.getElementById('age-max-val').textContent = val >= 100 ? '100+' : val;
        }});

        function applyFilters() {{
            var minApps = parseInt(document.getElementById('filter-apps-min').value);
            var maxPrice = parseInt(document.getElementById('filter-price-max').value);
            var maxDist = parseInt(document.getElementById('filter-dist-max').value);
            var maxAge = parseInt(document.getElementById('filter-age-max').value);

            // Filter properties
            var visibleCount = 0;
            var visiblePropertyIds = [];

            properties.forEach(function(prop) {{
                var visible = true;

                if (prop.apps < minApps) visible = false;
                if (prop.price !== null && prop.price > maxPrice) visible = false;
                if (prop.dist !== null && prop.dist > maxDist) visible = false;
                if (prop.age !== null && prop.age > maxAge) visible = false;

                // Find and hide/show marker
                var markers = document.querySelectorAll('[data-property-id="' + prop.id + '"]');
                markers.forEach(function(marker) {{
                    var parent = marker.closest('.leaflet-marker-icon');
                    if (parent) {{
                        parent.style.display = visible ? 'block' : 'none';
                    }}
                }});

                if (visible) {{
                    visibleCount++;
                    visiblePropertyIds.push(prop.id);
                }}
            }});

            // Filter flow lines - hide flows for hidden properties
            var allFlowLines = document.querySelectorAll('path.flow-line');
            allFlowLines.forEach(function(path) {{
                var pathClasses = path.getAttribute('class') || '';
                var isVisible = false;

                // Check if this flow line belongs to any visible property
                visiblePropertyIds.forEach(function(propId) {{
                    if (pathClasses.includes('prop-' + propId)) {{
                        isVisible = true;
                    }}
                }});

                // Set display without affecting highlighting styles
                path.style.display = isVisible ? '' : 'none';
            }});

            // Hide applicant origin circles when filtering (since they're not property-specific)
            var anyFiltering = visibleCount < properties.length;
            var originCircles = document.querySelectorAll('.leaflet-interactive[fill="#3B82F6"]');
            originCircles.forEach(function(circle) {{
                // Only hide circles, not flow lines (flow lines also have fill but are paths)
                if (circle.tagName.toLowerCase() === 'circle') {{
                    circle.style.display = anyFiltering ? 'none' : '';
                }}
            }});

            alert('Filters applied! Showing ' + visibleCount + ' of ' + properties.length + ' properties.');
        }}

        function resetFilters() {{
            document.getElementById('filter-apps-min').value = 0;
            document.getElementById('filter-price-max').value = 500000;
            document.getElementById('filter-dist-max').value = 100;
            document.getElementById('filter-age-max').value = 100;
            document.getElementById('apps-min-val').textContent = '0';
            document.getElementById('price-max-val').textContent = '$500K+';
            document.getElementById('dist-max-val').textContent = '100+';
            document.getElementById('age-max-val').textContent = '100+';

            // Show all markers
            document.querySelectorAll('.leaflet-marker-icon').forEach(function(marker) {{
                marker.style.display = 'block';
            }});

            // Show all flow lines
            var allFlowLines = document.querySelectorAll('path.flow-line');
            allFlowLines.forEach(function(path) {{
                path.style.display = '';  // Reset to default (visible)
            }});

            // Show all applicant origin circles
            var originCircles = document.querySelectorAll('.leaflet-interactive[fill="#3B82F6"]');
            originCircles.forEach(function(circle) {{
                if (circle.tagName.toLowerCase() === 'circle') {{
                    circle.style.display = '';  // Reset to default (visible)
                }}
            }});
        }}
        </script>
        """

        m.get_root().html.add_child(folium.Element(custom_html))

        # Save
        output_path = os.path.join(outdir, "applications_map_enhanced.html")
        m.save(output_path)
        logging.info(f"Enhanced map saved to {output_path}")

    except Exception as e:
        logging.error(f"Map creation failed: {e}", exc_info=True)
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description="Generate enhanced interactive folium map")
    parser.add_argument("--input", required=True, help="Path to applications file")
    parser.add_argument("--outdir", default=DEFAULT_OUTPUT, help="Output directory")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    ensure_dir(args.outdir)

    logging.info(f"Reading {args.input}")
    df = read_any(args.input)

    if PROP_LAT_COL not in df.columns or PROP_LON_COL not in df.columns:
        logging.error("Property coordinates not found!")
        return

    prop_geo_count = df[[PROP_LAT_COL, PROP_LON_COL]].notna().all(axis=1).sum()
    logging.info(f"Found property coordinates for {prop_geo_count}/{len(df)} applications")

    # Load bedroom data
    logging.info("Loading bedroom data from resale transaction files...")
    bedroom_map = load_bedroom_data()

    demand, attrs = build_property_tables(df, bedroom_map)
    demand = demand.merge(attrs, on="Property", how="left")

    out_csv = os.path.join(args.outdir, "property_demand_with_geo.csv")
    demand.to_csv(out_csv, index=False)
    logging.info(f"Saved {out_csv}")

    logging.info("Creating enhanced interactive map...")
    plot_v4_enhanced_map(demand, df, args.outdir)

    logging.info("Done!")

if __name__ == "__main__":
    main()
