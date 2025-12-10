#!/usr/bin/env python3
"""
Property Popularity Graph Generation

Generates statistical visualizations for property popularity analysis:
- Price vs. application volume relationship
- Top properties bar charts (overall and by demographics)
- Pareto chart showing concentration of applications
- Trait analysis of most popular properties

Inputs
------
--input   : data/processed/applications_clean.parquet
--outdir  : output folder for CSVs and figures (default: visuals)

Outputs
-------
- property_demand_with_geo.csv : Property-level data with coordinates
- applications_vs_price_binned.png : Price vs demand scatter/line chart
- top_properties_bar.png : Top 15 properties bar chart
- top_properties_stacked.png : Top 15 properties stacked by race
- applications_pareto.png : Pareto chart of application concentration
- popular_property_traits_analysis.csv : Statistical comparison of traits for popular vs all properties
- popular_property_traits_comparison.png : Box plots comparing trait distributions
"""

from __future__ import annotations

import argparse
import logging
import os
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import binned_statistic
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import StrMethodFormatter

# -----------------------
# Config
# -----------------------
DEFAULT_OUTPUT = "visuals/Portfolio Effects Analysis"
PROP_COL = "Application Property"
PRICE_COL = "Property Maximum Resale Price"

# Property coordinates
PROP_LON_COL = "property_longitude"
PROP_LAT_COL = "property_latitude"

# Applicant residence coordinates
APPLICANT_LON_COL = "longitude"
APPLICANT_LAT_COL = "latitude"

# Demographic columns
DEMO_COLS = {
    "dummy_asian": ("Asian", "#F59E0B"),  # amber-500
    "dummy_black_african_american": ("Black/African American", "#0F766E"),  # teal-700
    "dummy_hispanic": ("Hispanic/Latine", "#7C3AED"),  # violet-600
    "dummy_white": ("White", "#2563EB"),  # blue-600
    "dummy_native_american_alaskan_native": ("Native American/Alaskan Native", "#DC2626"),  # red-600
    "dummy_white_MENA": ("White (MENA)", "#0891B2"),  # cyan-600
    "dummy_choose_not_to_answer": ("Prefer not to say", "#6B7280"),  # gray-500
    "dummy_unknown": ("Unknown", "#94A3B8"),  # slate-400
}

# -----------------------
# IO Helpers
# -----------------------

def read_any(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file extension for {path}")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# -----------------------
# Utilities
# -----------------------

def to_float_series(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in miles"""
    from math import radians, cos, sin, asin, sqrt

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth in miles
    r = 3956
    return c * r


def load_bedroom_data() -> dict:
    """Load bedroom and age restriction data from resale transaction info files"""
    property_data = {}

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
                xl = pd.ExcelFile(file_path)
                sheet_name = 'final_round2' if 'final_round2' in xl.sheet_names else xl.sheet_names[0]
                df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Check if required columns exist
            if 'Bedrooms' not in df.columns:
                continue

            # Match based on Address and City columns
            if 'Address' in df.columns and 'City' in df.columns:
                for _, row in df.iterrows():
                    if pd.notna(row.get('Address')) and pd.notna(row.get('City')):
                        address = str(row['Address']).strip()
                        city = str(row['City']).strip()

                        # Normalize the address for matching
                        address_normalized = address.lower()
                        address_normalized = address_normalized.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
                        address_normalized = address_normalized.replace(' drive', ' dr').replace(' lane', ' ln')
                        address_normalized = address_normalized.replace(' st.', ' st').replace(' rd.', ' rd').replace(' ave.', ' ave')
                        address_normalized = address_normalized.replace(' dr.', ' dr').replace(' ln.', ' ln')
                        address_normalized = address_normalized.rstrip(',.').strip()
                        city_normalized = city.lower()

                        key = f"{address_normalized} ~ {city_normalized}"

                        if key not in property_data:
                            property_data[key] = {
                                'bedrooms': [],
                                'age_restricted': []
                            }

                        if pd.notna(row.get('Bedrooms')):
                            property_data[key]['bedrooms'].append(int(row['Bedrooms']))

                        if pd.notna(row.get('Age Restricted')):
                            property_data[key]['age_restricted'].append(str(row['Age Restricted']))

            logging.info(f"Loaded property data from {file_path}: {len(property_data)} unique properties")
        except Exception as e:
            logging.warning(f"Could not load property data from {file_path}: {e}")

    # Convert lists to mode (most common value)
    from scipy import stats
    from collections import Counter
    property_map = {}
    for prop_key, data in property_data.items():
        property_map[prop_key] = {}

        if data['bedrooms']:
            mode_result = stats.mode(data['bedrooms'], keepdims=True)
            property_map[prop_key]['bedrooms'] = int(mode_result.mode[0])

        if data['age_restricted']:
            # Use Counter for string data instead of stats.mode
            counter = Counter(data['age_restricted'])
            property_map[prop_key]['age_restricted'] = counter.most_common(1)[0][0]

    logging.info(f"Created property mapping for {len(property_map)} properties")
    return property_map


def normalize_property_for_match(property_str: str) -> str:
    """Normalize an Application Property string to match property_map keys"""
    if pd.isna(property_str):
        return None

    prop_str = str(property_str).lower().strip()
    import re

    # Fix cases where there's no space after ~
    prop_str = re.sub(r'~(?!\s)', '~ ', prop_str)

    if ' ~ ' in prop_str:
        parts = prop_str.split(' ~ ')
        if len(parts) == 2:
            address_part = parts[0].strip()
            city_part = parts[1].strip()

            # Remove unit numbers from address
            address_part = re.sub(r',?\s+unit\s+#?\s*[\w\-]+', '', address_part, flags=re.IGNORECASE)
            address_part = re.sub(r',?\s*#\s*[\w\-]+', '', address_part)
            address_part = re.sub(r',\s*[a-z]\d+,?', '', address_part, flags=re.IGNORECASE)
            address_part = re.sub(r',\s+unit\s+[\w\-]+$', '', address_part, flags=re.IGNORECASE)

            # Normalize street types
            address_part = address_part.replace(' street', ' st').replace(' road', ' rd').replace(' avenue', ' ave')
            address_part = address_part.replace(' drive', ' dr').replace(' lane', ' ln')
            address_part = address_part.replace(' st.', ' st').replace(' rd.', ' rd').replace(' ave.', ' ave')
            address_part = address_part.replace(' dr.', ' dr').replace(' ln.', ' ln')
            address_part = address_part.rstrip(',.').strip()

            # Clean city part
            city_part = re.sub(r'\s*\(.*?\)', '', city_part).strip()

            return f"{address_part} ~ {city_part}"

    return None


def build_property_tables(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return (demand, attrs) dataframes, both one row per property.

    demand: Property, application_count
    attrs : Property, price_num, property_longitude, property_latitude,
            applicant_median_lon, applicant_median_lat, median_distance_miles,
            plus applicant-level aggregates (age, HH size, income, etc.)

    NOTE: Property coordinates are now in the main dataset (property_latitude, property_longitude)
    """
    if PROP_COL not in df.columns:
        raise KeyError(f"Missing required column: {PROP_COL}")

    # Check for property coordinates in dataset
    if PROP_LAT_COL not in df.columns or PROP_LON_COL not in df.columns:
        raise KeyError(
            f"Property coordinates not found in dataset. "
            f"Expected columns: {PROP_LAT_COL}, {PROP_LON_COL}. "
            f"Run PYTHONPATH=. python scripts/06_clean_applications_pipeline.py"
        )

    # Demand: count applications per property
    demand = (
        df.groupby(PROP_COL)
          .size()
          .reset_index(name="application_count")
          .rename(columns={PROP_COL: "Property"})
          .sort_values("application_count", ascending=False)
    )

    # Load property-level data (bedrooms, age restriction)
    logging.info("Loading property-level data (bedrooms, age restriction)...")
    property_map = load_bedroom_data()

    # Add property-level data to demand
    demand['property_normalized'] = demand['Property'].apply(normalize_property_for_match)
    demand['bedrooms'] = demand['property_normalized'].apply(
        lambda x: property_map.get(x, {}).get('bedrooms') if x else None
    )
    demand['age_restricted'] = demand['property_normalized'].apply(
        lambda x: property_map.get(x, {}).get('age_restricted') if x else None
    )
    demand.drop(columns=['property_normalized'], inplace=True)

    # Price attributes
    price_num = to_float_series(df[PRICE_COL]) if PRICE_COL in df.columns else pd.Series([np.nan]*len(df))

    # Applicant residence coordinates (for comparison/distance viz)
    applicant_lon = to_float_series(df[APPLICANT_LON_COL]) if APPLICANT_LON_COL in df.columns else pd.Series([np.nan]*len(df))
    applicant_lat = to_float_series(df[APPLICANT_LAT_COL]) if APPLICANT_LAT_COL in df.columns else pd.Series([np.nan]*len(df))

    # Property coordinates (already in dataset)
    prop_lon = to_float_series(df[PROP_LON_COL])
    prop_lat = to_float_series(df[PROP_LAT_COL])

    # Extract applicant-level features
    age_data = to_float_series(df['Age']) if 'Age' in df.columns else pd.Series([np.nan]*len(df))
    hh_size_data = to_float_series(df['HH Size']) if 'HH Size' in df.columns else pd.Series([np.nan]*len(df))
    dependents_data = to_float_series(df['Dependents']) if 'Dependents' in df.columns else pd.Series([np.nan]*len(df))
    hh_income_data = to_float_series(df['HH Income']) if 'HH Income' in df.columns else pd.Series([np.nan]*len(df))
    hh_assets_data = to_float_series(df['HH Assets']) if 'HH Assets' in df.columns else pd.Series([np.nan]*len(df))

    # Disability is typically Yes/No, convert to binary
    disability_data = pd.Series([np.nan]*len(df))
    if 'Disability' in df.columns:
        disability_data = df['Disability'].map({'Yes': 1, 'No': 0}).fillna(np.nan)

    # FTHB Class is typically Yes/No, convert to binary
    fthb_data = pd.Series([np.nan]*len(df))
    if 'FTHB Class?' in df.columns:
        fthb_data = df['FTHB Class?'].map({'Yes': 1, 'No': 0}).fillna(np.nan)

    # Build aggregation dictionary
    agg_dict = {
        "price_num": ("price_num", "median"),
        "applicant_median_lon": ("applicant_median_lon", "median"),
        "applicant_median_lat": ("applicant_median_lat", "median"),
        "property_longitude": (PROP_LON_COL, "first"),
        "property_latitude": (PROP_LAT_COL, "first"),
    }

    # Add applicant-level aggregations
    if 'Age' in df.columns:
        agg_dict["median_age"] = ("age_data", "median")
        agg_dict["mean_age"] = ("age_data", "mean")

    if 'HH Size' in df.columns:
        agg_dict["median_hh_size"] = ("hh_size_data", "median")
        agg_dict["mean_hh_size"] = ("hh_size_data", "mean")

    if 'Dependents' in df.columns:
        agg_dict["median_dependents"] = ("dependents_data", "median")
        agg_dict["mean_dependents"] = ("dependents_data", "mean")

    if 'HH Income' in df.columns:
        agg_dict["median_hh_income"] = ("hh_income_data", "median")
        agg_dict["mean_hh_income"] = ("hh_income_data", "mean")

    if 'HH Assets' in df.columns:
        agg_dict["median_hh_assets"] = ("hh_assets_data", "median")
        agg_dict["mean_hh_assets"] = ("hh_assets_data", "mean")

    if 'Disability' in df.columns:
        agg_dict["pct_disability"] = ("disability_data", "mean")  # Proportion with disability

    if 'FTHB Class?' in df.columns:
        agg_dict["pct_fthb"] = ("fthb_data", "mean")  # Proportion first-time homebuyers

    attrs = (
        pd.DataFrame({
            PROP_COL: df[PROP_COL],
            "price_num": price_num,
            "applicant_median_lon": applicant_lon,
            "applicant_median_lat": applicant_lat,
            PROP_LON_COL: prop_lon,
            PROP_LAT_COL: prop_lat,
            "age_data": age_data,
            "hh_size_data": hh_size_data,
            "dependents_data": dependents_data,
            "hh_income_data": hh_income_data,
            "hh_assets_data": hh_assets_data,
            "disability_data": disability_data,
            "fthb_data": fthb_data,
        })
        .groupby(PROP_COL, as_index=False)
        .agg(**agg_dict)
        .rename(columns={PROP_COL: "Property"})
    )

    # Calculate median distance from applicants to property
    distances = []
    for _, row in df.iterrows():
        if pd.notna(row[PROP_LAT_COL]) and pd.notna(row[PROP_LON_COL]) and \
           pd.notna(row[APPLICANT_LAT_COL]) and pd.notna(row[APPLICANT_LON_COL]):
            dist = haversine_distance(
                row[APPLICANT_LAT_COL], row[APPLICANT_LON_COL],
                row[PROP_LAT_COL], row[PROP_LON_COL]
            )
            distances.append({
                "Property": row[PROP_COL],
                "distance_miles": dist
            })

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
        attrs["median_distance_miles"] = np.nan
        attrs["avg_distance_miles"] = np.nan
        attrs["min_distance_miles"] = np.nan
        attrs["max_distance_miles"] = np.nan

    return demand, attrs


# -----------------------
# Visuals
# -----------------------

def plot_price_vs_demand(demand: pd.DataFrame, outdir: str) -> None:
    """Show relationship between price and application volume using binned means"""
    if demand.empty or "price_num" not in demand.columns:
        return

    df = demand.dropna(subset=["price_num", "application_count"]).copy()
    df = df[df["price_num"] > 0]
    df["price_log"] = np.log10(df["price_num"])

    n_bins = 8
    bins = np.linspace(df["price_log"].min(), df["price_log"].max(), n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    mean_apps, _, _ = binned_statistic(df["price_log"], df["application_count"], statistic="mean", bins=bins)

    from statsmodels.nonparametric.smoothers_lowess import lowess
    smoothed = lowess(mean_apps, bin_centers, frac=0.7, return_sorted=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["price_num"], df["application_count"], alpha=0.35, s=35, color="#64748B", label="Individual properties")
    ax.plot(10 ** bin_centers, smoothed, color="#0F766E", linewidth=2.5, label="Smoothed mean (by price bin)")
    ax.plot(10 ** bin_centers, mean_apps, "o", color="#0F766E", markersize=6, alpha=0.8)

    ax.set_xscale("log")
    ax.set_xlabel("Maximum Resale Price ($, log scale)", fontsize=11)
    ax.set_ylabel("Applications per Property", fontsize=11)
    ax.set_title("Relationship Between Price and Application Volume", fontsize=14, weight="bold")
    ax.grid(True, which="major", linestyle="--", color="#E2E8F0", linewidth=0.8, alpha=0.8)
    ax.legend(frameon=False, loc="upper right")

    slope = np.gradient(smoothed, bin_centers)
    if len(slope) > 0 and slope[-1] < 0:
        ax.annotate("Higher prices show reduced demand", xy=(10 ** bin_centers[-2], smoothed[-2]),
                    xytext=(10 ** bin_centers[-3], smoothed[-2] + 3),
                    arrowprops=dict(arrowstyle="->", color="#475569"), fontsize=10, color="#334155",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1", alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "applications_vs_price_binned.png"), dpi=220)
    plt.close()


def plot_top_properties(demand: pd.DataFrame, outdir: str, top_n: int = 15) -> None:
    top = demand.head(top_n).copy()
    if top.empty:
        return

    top["label"] = top["Property"].str.slice(0, 45)
    fig, ax = plt.subplots(figsize=(13, 7))

    bars = ax.barh(top["label"], top["application_count"], color="#CBD5E1", edgecolor="#94A3B8",
                   linewidth=0.6, alpha=0.95, zorder=2)
    for i, bar in enumerate(bars):
        if i < 3:
            bar.set_color("#0F766E")
            bar.set_edgecolor("#0F766E")

    ax.invert_yaxis()
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in top["application_count"]], padding=4,
                 fontsize=10, color="#334155")

    ax.set_xlabel("Applications per Property", fontsize=11)
    ax.set_ylabel("Property", fontsize=11)
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.grid(True, axis="x", color="#E2E8F0", linewidth=0.8)
    ax.grid(False, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title("Top Properties by Application Volume", fontsize=14, weight="bold", loc="left")
    fig.suptitle("Bars = Applications · Sorted most to least", y=0.98, x=0.01, ha="left",
                 fontsize=10, color="#475569")

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig(os.path.join(outdir, "top_properties_bar.png"), dpi=220)
    plt.close()


def plot_top_properties_stacked(demand: pd.DataFrame, df: pd.DataFrame, outdir: str, top_n: int = 15) -> None:
    """Stacked bar chart by race for top properties"""
    if demand.empty or df.empty:
        return

    prop_col_df = "Application Property" if "Application Property" in df.columns else "Property"

    race_cols = [(c, lbl, col) for c, (lbl, col) in DEMO_COLS.items() if c in df.columns]
    if not race_cols:
        print("No race columns found — skipping stacked chart.")
        return

    race_counts = (
        df.groupby(prop_col_df)[[c for c, _, _ in race_cols]]
          .sum()
          .reset_index()
          .rename(columns={prop_col_df: "Property"})
    )

    top = (
        demand[["Property", "application_count"]]
        .sort_values("application_count", ascending=False)
        .head(top_n)
        .merge(race_counts, on="Property", how="left")
        .fillna(0)
        .copy()
    )

    top["label"] = top["Property"].str.slice(0, 45)
    top = top.sort_values("application_count", ascending=False)

    fig, ax = plt.subplots(figsize=(13, 7))

    left = np.zeros(len(top))
    for c, lbl, color in race_cols:
        vals = top[c].astype(float).values
        ax.barh(top["label"], vals, left=left, color=color, edgecolor="white",
                linewidth=0.5, alpha=0.95, label=lbl, zorder=2)
        left += vals

    ax.invert_yaxis()

    totals = top["application_count"].astype(int).values
    for y, total in enumerate(totals):
        ax.text(left[y] + max(totals)*0.01, y, f"{total:,.0f}", va="center",
                fontsize=10, color="#334155")

    ax.set_xlabel("Applications per Property", fontsize=11)
    ax.set_ylabel("Property", fontsize=11)
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.grid(True, axis="x", color="#E2E8F0", linewidth=0.8)
    ax.grid(False, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title("Top Properties by Application Volume (Stacked by Race)", fontsize=14, weight="bold", loc="left")
    fig.suptitle("Stack segments show application counts by race; totals shown at bar ends",
                 y=0.98, x=0.01, ha="left", fontsize=10, color="#475569")

    ax.legend(frameon=False, bbox_to_anchor=(1.02, 1), loc="upper left",
              borderaxespad=0.0, title="Race")

    plt.tight_layout()
    plt.subplots_adjust(right=0.80, top=0.92)
    plt.savefig(os.path.join(outdir, "top_properties_stacked.png"), dpi=220)
    plt.close()


def plot_pareto(demand: pd.DataFrame, outdir: str) -> None:
    if demand.empty:
        return

    d = demand.sort_values("application_count", ascending=False).copy()
    d["cum_apps"] = d["application_count"].cumsum() / d["application_count"].sum()
    d["idx"] = np.arange(1, len(d) + 1)
    d["cum_props"] = d["idx"] / len(d)

    eighty_idx = int(np.searchsorted(d["cum_apps"].values, 0.80))
    eighty_prop_share = d.iloc[eighty_idx]["cum_props"] if len(d) > 0 else np.nan
    x80 = d.iloc[eighty_idx]["idx"]

    markevery = max(1, len(d) // 30)

    fig, ax1 = plt.subplots(figsize=(13, 7))

    ax1.bar(d["idx"], d["application_count"], width=0.9, color="#CBD5E1",
            edgecolor="#94A3B8", linewidth=0.3, alpha=0.95, zorder=1)
    ax1.set_ylabel("Applications per Property", fontsize=11)
    ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    ax2 = ax1.twinx()
    ax2.plot(d["idx"], d["cum_apps"], color="#0F766E", linewidth=2, marker="o",
             markersize=4, markevery=markevery, markerfacecolor="white",
             markeredgewidth=0.8, zorder=3, label="Cumulative share")
    ax2.set_ylim(0, 1.02)
    ax2.set_ylabel("Cumulative Share of Applications", fontsize=11)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax2.axhline(0.80, color="#94A3B8", linestyle="--", linewidth=1, zorder=0)
    ax1.axvline(x80, color="#94A3B8", linestyle="--", linewidth=1, zorder=0)
    ax2.plot([1, len(d)], [0, 1], linestyle="--", linewidth=1, color="#E2E8F0", zorder=0)

    if np.isfinite(eighty_prop_share):
        ax2.annotate(f"≈{eighty_prop_share*100:.0f}% of properties\naccount for 80% of applications",
                     xy=(x80, 0.80),
                     xytext=(min(x80 + max(5, int(len(d)*0.06)), int(len(d)*0.92)), 0.88),
                     arrowprops=dict(arrowstyle="->", lw=1, color="#475569"),
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1", alpha=0.9),
                     fontsize=10, ha="left", va="bottom", color="#334155")

    if len(d) > 30:
        ax1.set_xticks(np.linspace(1, len(d), 6).astype(int))
    else:
        ax1.set_xticks(d["idx"])

    ax1.set_xlabel("Properties (sorted by applications, most to least)", fontsize=11)
    plt.title("Pareto of Applications by Property", fontsize=14, weight="bold", loc="left")
    fig.suptitle("Bars = Applications · Line = Cumulative Share", y=0.98, x=0.01,
                 ha="left", fontsize=10, color="#475569")

    ax1.grid(True, axis="y", color="#E2E8F0", linewidth=0.8)
    ax1.grid(False, axis="x")
    ax2.grid(False)

    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)

    ax2.legend(frameon=False, loc="lower right")

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig(os.path.join(outdir, "applications_pareto.png"), dpi=220)
    plt.close()


def analyze_popular_property_traits(demand: pd.DataFrame, outdir: str, top_n: int = 20, top_percentile: int = 10) -> pd.DataFrame:
    """
    Analyze traits of the most popular properties vs all properties.

    Returns a DataFrame with comparative statistics.
    """
    if demand.empty:
        return pd.DataFrame()

    # Define "popular" properties - using both top N and top percentile
    top_by_count = demand.nlargest(top_n, "application_count")
    percentile_threshold = demand["application_count"].quantile(1 - top_percentile / 100)
    top_by_percentile = demand[demand["application_count"] >= percentile_threshold]

    # Use the larger of the two sets
    popular = top_by_percentile if len(top_by_percentile) > len(top_by_count) else top_by_count
    all_props = demand

    # Traits to analyze - expanded list
    trait_cols = [
        # Property characteristics
        "price_num",
        # Distance metrics
        "median_distance_miles", "avg_distance_miles",
        "min_distance_miles", "max_distance_miles",
        # Applicant age
        "mean_age",
        # Household characteristics
        "mean_hh_size",
        "mean_dependents",
        # Financial characteristics
        "median_hh_income",
        "median_hh_assets", "mean_hh_assets",
        # Binary characteristics (proportions)
        "pct_disability", "pct_fthb",
        # Location (for reference)
        "property_latitude", "property_longitude"
    ]

    # Filter to existing columns
    trait_cols = [c for c in trait_cols if c in demand.columns]

    results = []

    for trait in trait_cols:
        popular_vals = popular[trait].dropna()
        all_vals = all_props[trait].dropna()

        if len(popular_vals) == 0 or len(all_vals) == 0:
            continue

        result = {
            "Trait": trait,
            "Popular_Mean": popular_vals.mean(),
            "Popular_Median": popular_vals.median(),
            "Popular_Std": popular_vals.std(),
            "All_Mean": all_vals.mean(),
            "All_Median": all_vals.median(),
            "All_Std": all_vals.std(),
            "Difference_Mean": popular_vals.mean() - all_vals.mean(),
            "Difference_Median": popular_vals.median() - all_vals.median(),
            "Percent_Diff_Mean": ((popular_vals.mean() - all_vals.mean()) / all_vals.mean() * 100) if all_vals.mean() != 0 else np.nan,
        }

        # Perform t-test if we have enough data
        if len(popular_vals) >= 2 and len(all_vals) >= 2:
            from scipy import stats
            t_stat, p_value = stats.ttest_ind(popular_vals, all_vals, equal_var=False)
            result["T_Statistic"] = t_stat
            result["P_Value"] = p_value
            result["Significant"] = "Yes" if p_value < 0.05 else "No"

        results.append(result)

    # Add application count statistics
    results.append({
        "Trait": "application_count",
        "Popular_Mean": popular["application_count"].mean(),
        "Popular_Median": popular["application_count"].median(),
        "Popular_Std": popular["application_count"].std(),
        "All_Mean": all_props["application_count"].mean(),
        "All_Median": all_props["application_count"].median(),
        "All_Std": all_props["application_count"].std(),
        "Difference_Mean": popular["application_count"].mean() - all_props["application_count"].mean(),
        "Difference_Median": popular["application_count"].median() - all_props["application_count"].median(),
        "Percent_Diff_Mean": ((popular["application_count"].mean() - all_props["application_count"].mean()) / all_props["application_count"].mean() * 100),
    })

    trait_analysis = pd.DataFrame(results)

    # Save to CSV
    out_csv = os.path.join(outdir, "popular_property_traits_analysis.csv")
    trait_analysis.to_csv(out_csv, index=False)
    logging.info(f"Saved trait analysis to {out_csv}")

    # Log summary
    logging.info(f"\n{'='*70}")
    logging.info(f"POPULAR PROPERTY TRAITS ANALYSIS")
    logging.info(f"{'='*70}")
    logging.info(f"Comparing top {len(popular)} properties (top {top_percentile}%) vs all {len(all_props)} properties")
    logging.info(f"\nKey Findings:")

    for _, row in trait_analysis.iterrows():
        trait = row["Trait"]
        if pd.notna(row.get("Percent_Diff_Mean")):
            direction = "higher" if row["Percent_Diff_Mean"] > 0 else "lower"
            sig = f" (p={row['P_Value']:.4f})" if "P_Value" in row and pd.notna(row["P_Value"]) else ""
            logging.info(f"  • {trait}: {abs(row['Percent_Diff_Mean']):.1f}% {direction} on average{sig}")

    logging.info(f"{'='*70}\n")

    return trait_analysis


def plot_trait_comparison(demand: pd.DataFrame, outdir: str, top_percentile: int = 10) -> None:
    """Create individual visualizations comparing traits of popular vs all properties"""
    if demand.empty:
        return

    # Define popular properties
    percentile_threshold = demand["application_count"].quantile(1 - top_percentile / 100)
    demand_copy = demand.copy()
    demand_copy["Category"] = demand_copy["application_count"].apply(
        lambda x: f"Top {top_percentile}%" if x >= percentile_threshold else f"Other {100-top_percentile}%"
    )

    # Expanded traits to visualize - each will be a separate image
    traits = [
        # Property characteristics
        ("price_num", "Maximum Resale Price ($)", True, "price"),
        # Distance metrics
        ("median_distance_miles", "Median Distance from Applicants (miles)", False, "distance_median"),
        ("avg_distance_miles", "Average Distance from Applicants (miles)", False, "distance_avg"),
        # Applicant age
        ("mean_age", "Mean Applicant Age (years)", False, "age_mean"),
        # Household characteristics
        ("mean_hh_size", "Mean Household Size", False, "hh_size_mean"),
        ("mean_dependents", "Mean Number of Dependents", False, "dependents_mean"),
        # Financial characteristics
        ("median_hh_income", "Median Household Income ($)", False, "hh_income_median"),
        ("median_hh_assets", "Median Household Assets ($)", False, "hh_assets_median"),
        ("mean_hh_assets", "Mean Household Assets ($)", False, "hh_assets_mean"),
        # Proportions
        ("pct_disability", "Proportion with Disability", False, "disability_pct"),
        ("pct_fthb", "Proportion First-Time Homebuyers", False, "fthb_pct"),
    ]

    # Filter to traits that exist
    traits = [(col, label, log, filename) for col, label, log, filename in traits if col in demand_copy.columns]

    if not traits:
        logging.warning("No trait columns found for visualization")
        return

    logging.info(f"Generating {len(traits)} individual trait comparison plots...")

    # Create individual plots for each trait
    for trait_col, trait_label, use_log, filename in traits:
        data_to_plot = demand_copy[[trait_col, "Category"]].dropna()

        if data_to_plot.empty:
            logging.warning(f"No data for trait: {trait_col}")
            continue

        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))

        # Box plot
        categories = [f"Top {top_percentile}%", f"Other {100-top_percentile}%"]
        plot_data = [
            data_to_plot[data_to_plot["Category"] == cat][trait_col].values
            for cat in categories
        ]

        # Check if we have data for both categories
        if len(plot_data[0]) == 0 or len(plot_data[1]) == 0:
            logging.warning(f"Insufficient data for trait: {trait_col}")
            plt.close()
            continue

        bp = ax.boxplot(plot_data, labels=categories, patch_artist=True,
                       widths=0.6, showmeans=True,
                       boxprops=dict(facecolor="#CBD5E1", edgecolor="#475569", linewidth=1.2),
                       whiskerprops=dict(color="#475569", linewidth=1.2),
                       capprops=dict(color="#475569", linewidth=1.2),
                       medianprops=dict(color="#0F766E", linewidth=2),
                       meanprops=dict(marker="D", markerfacecolor="#DC2626",
                                     markeredgecolor="#DC2626", markersize=6))

        # Highlight top percentile box
        bp['boxes'][0].set_facecolor('#0F766E')
        bp['boxes'][0].set_alpha(0.6)

        ax.set_ylabel(trait_label, fontsize=12, weight='bold')
        ax.set_xlabel("Property Category", fontsize=11)

        # Format y-axis based on trait type
        if use_log:
            ax.set_yscale("log")
            ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))
        elif 'income' in trait_col.lower() or 'assets' in trait_col.lower() or 'price' in trait_col.lower():
            ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))
        elif 'pct' in trait_col.lower():
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        else:
            ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.1f}"))

        ax.grid(True, axis="y", color="#E2E8F0", linewidth=0.8, alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Update x-tick labels to include counts
        new_labels = [f"{cat}\n(n={len(plot_data[i])})" for i, cat in enumerate(categories)]
        ax.set_xticklabels(new_labels, fontsize=10)

        # Add title and subtitle
        ax.set_title(f"Comparison: {trait_label}", fontsize=14, weight="bold", pad=15)

        # Add statistical annotation if significantly different
        try:
            from scipy import stats
            if len(plot_data[0]) >= 2 and len(plot_data[1]) >= 2:
                t_stat, p_value = stats.ttest_ind(plot_data[0], plot_data[1], equal_var=False)
                if p_value < 0.05:
                    sig_text = f"Statistically significant difference (p={p_value:.4f})"
                    ax.text(0.5, 0.98, sig_text, transform=ax.transAxes,
                           ha="center", va="top", fontsize=9, color="#DC2626",
                           bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#DC2626", alpha=0.8))
        except Exception as e:
            logging.warning(f"Could not perform t-test for {trait_col}: {e}")

        plt.tight_layout()
        # Increase bottom margin to prevent overlap
        plt.subplots_adjust(bottom=0.18)

        # Add legend text at the bottom with proper spacing
        fig.text(0.5, 0.03, "Box = IQR · Line = Median · Diamond = Mean",
                ha="center", fontsize=9, color="#475569")

        # Save individual plot
        output_path = os.path.join(outdir, f"trait_comparison_{filename}.png")
        plt.savefig(output_path, dpi=220)
        plt.close()
        logging.info(f"  Generated: {output_path}")

    logging.info(f"Completed generating {len(traits)} trait comparison visualizations")


# -----------------------
# Main
# -----------------------

def main():
    parser = argparse.ArgumentParser(description="Generate property popularity graphs and charts")
    parser.add_argument("--input", required=True, help="Path to applications file (CSV/Parquet/Excel)")
    parser.add_argument("--outdir", default=DEFAULT_OUTPUT, help="Directory to save outputs & figures")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    ensure_dir(args.outdir)

    logging.info(f"Reading {args.input}")
    df = read_any(args.input)

    # Verify property coordinates are in dataset
    if PROP_LAT_COL not in df.columns or PROP_LON_COL not in df.columns:
        logging.error(f"Property coordinates not found in dataset!")
        logging.error(f"Expected columns: {PROP_LAT_COL}, {PROP_LON_COL}")
        logging.error("Please run: PYTHONPATH=. python scripts/06_clean_applications_pipeline.py")
        return

    prop_geo_count = df[[PROP_LAT_COL, PROP_LON_COL]].notna().all(axis=1).sum()
    logging.info(f"Found property coordinates for {prop_geo_count}/{len(df)} applications ({prop_geo_count/len(df)*100:.1f}%)")

    # Build per-property demand and attributes
    demand, attrs = build_property_tables(df)
    demand = demand.merge(attrs, on="Property", how="left")

    # Save enriched table
    out_csv = os.path.join(args.outdir, "property_demand_with_geo.csv")
    demand.to_csv(out_csv, index=False)
    logging.info(f"Saved {out_csv} ({len(demand)} rows)")

    # Create visualizations
    logging.info("Generating visualizations...")
    plot_top_properties(demand, args.outdir, top_n=15)
    plot_pareto(demand, args.outdir)
    plot_price_vs_demand(demand, args.outdir)
    plot_top_properties_stacked(demand, df, args.outdir, top_n=15)

    # Analyze popular property traits
    logging.info("Analyzing traits of popular properties...")
    analyze_popular_property_traits(demand, args.outdir, top_n=20, top_percentile=10)
    plot_trait_comparison(demand, args.outdir, top_percentile=10)

    logging.info("Done!")


if __name__ == "__main__":
    main()
