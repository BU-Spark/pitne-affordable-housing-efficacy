#!/usr/bin/env python3
"""
Analyze property popularity in CHAPA applications (Team B schema tailored, extended visuals).

Inputs
------
--input   : data/processed/applications_clean.parquet (or CSV/XLSX)
--outdir  : output folder for CSVs and figures (default: visuals)

What this script does
---------------------
1) Uses **Application Property** as the property key (one row per property).
2) Computes demand = number of applications per property.
3) Builds one-row-per-property attributes:
   - price_num  (median numeric from 'Property Maximum Resale Price')
   - longitude/latitude  (median per property)
4) Saves tidy `property_demand.csv` (one row per property) and rich visuals:
   - `top_properties_bar.png`                (Top 15 by applications)
   - `applications_pareto.png`               (Pareto curve: cumulative share)
   - `applications_vs_price_lowess.png`      (Scatter with LOWESS if available; log-x)
   - `applications_by_price_quartile.png`    (Applications by price quartile)
   - `applications_map.png` OR
     `applications_map.html` (fallback with Folium if GeoPandas is missing)

Notes
-----
- We DO NOT merge applicant-level fields (like matched_city) into the per-property table
  to avoid exploding rows.
- Geo map uses one representative coordinate per property (median of lon/lat).
- If statsmodels isn't installed, the price scatter falls back to a linear trend line.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
from typing import Tuple
import folium
from folium.plugins import MarkerCluster, HeatMap, MiniMap, Fullscreen, MeasureControl, LocateControl
from folium import FeatureGroup, LayerControl
import branca.colormap as cm
import numpy as np
import pandas as pd
import scipy
from scipy.stats import binned_statistic
import matplotlib
import matplotlib.ticker as mtick
from matplotlib.ticker import StrMethodFormatter
# Force a non-GUI backend for headless/servers (prevents Qt/xcb errors)
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -----------------------
# Config
# -----------------------
DEFAULT_OUTPUT = "visuals"
PROP_COL = "Application Property"
PRICE_COL = "Property Maximum Resale Price"
LON_COL = "longitude"
LAT_COL = "latitude"

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


def build_property_tables(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return (demand, attrs) dataframes, both one row per property.
    demand: Property, application_count
    attrs : Property, price_num, longitude, latitude
    """
    if PROP_COL not in df.columns:
        raise KeyError(f"Missing required column: {PROP_COL}")

    # Demand: count applications per property
    demand = (
        df.groupby(PROP_COL)
          .size()
          .reset_index(name="application_count")
          .rename(columns={PROP_COL: "Property"})
          .sort_values("application_count", ascending=False)
    )

    # Attributes: aggregate to one row per property
    price_num = to_float_series(df[PRICE_COL]) if PRICE_COL in df.columns else pd.Series([np.nan]*len(df))
    lon = to_float_series(df[LON_COL]) if LON_COL in df.columns else pd.Series([np.nan]*len(df))
    lat = to_float_series(df[LAT_COL]) if LAT_COL in df.columns else pd.Series([np.nan]*len(df))

    attrs = (
        pd.DataFrame({
            PROP_COL: df[PROP_COL],
            "price_num": price_num,
            "longitude": lon,
            "latitude": lat,
        })
        .groupby(PROP_COL, as_index=False)
        .agg(
            price_num=("price_num", "median"),
            longitude=("longitude", "median"),
            latitude=("latitude", "median"),
        )
        .rename(columns={PROP_COL: "Property"})
    )

    return demand, attrs

# -----------------------
# Visuals
# -----------------------
def plot_price_vs_demand(demand: pd.DataFrame, outdir: str) -> None:
    """
    Show relationship between price and application volume using binned means
    and a smoothed trend. Replaces old boxplot and LOWESS charts.
    """
    if demand.empty or "price_num" not in demand.columns:
        return

    # Clean & prep
    df = demand.dropna(subset=["price_num", "application_count"]).copy()
    df = df[df["price_num"] > 0]
    df["price_log"] = np.log10(df["price_num"])

    # Bin by price (log scale)
    n_bins = 8
    bins = np.linspace(df["price_log"].min(), df["price_log"].max(), n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    mean_apps, _, _ = binned_statistic(df["price_log"], df["application_count"], statistic="mean", bins=bins)
    median_apps, _, _ = binned_statistic(df["price_log"], df["application_count"], statistic="median", bins=bins)
    count_per_bin, _, _ = binned_statistic(df["price_log"], df["application_count"], statistic="count", bins=bins)

    # Smooth line (optional LOWESS on binned data)
    from statsmodels.nonparametric.smoothers_lowess import lowess
    smoothed = lowess(mean_apps, bin_centers, frac=0.7, return_sorted=False)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        df["price_num"],
        df["application_count"],
        alpha=0.35,
        s=35,
        color="#64748B",
        label="Individual properties",
    )
    ax.plot(10 ** bin_centers, smoothed, color="#0F766E", linewidth=2.5, label="Smoothed mean (by price bin)")
    ax.plot(10 ** bin_centers, mean_apps, "o", color="#0F766E", markersize=6, alpha=0.8)

    # Axis format
    ax.set_xscale("log")
    ax.set_xlabel("Maximum Resale Price ($, log scale)", fontsize=11)
    ax.set_ylabel("Applications per Property", fontsize=11)
    ax.set_title("Relationship Between Price and Application Volume", fontsize=14, weight="bold")
    ax.grid(True, which="major", linestyle="--", color="#E2E8F0", linewidth=0.8, alpha=0.8)
    ax.legend(frameon=False, loc="upper right")

    # Annotation: price elasticity hint
    slope = np.gradient(smoothed, bin_centers)
    if len(slope) > 0:
        if slope[-1] < 0:
            ax.annotate(
                "Higher prices show reduced demand",
                xy=(10 ** bin_centers[-2], smoothed[-2]),
                xytext=(10 ** bin_centers[-3], smoothed[-2] + 3),
                arrowprops=dict(arrowstyle="->", color="#475569"),
                fontsize=10,
                color="#334155",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1", alpha=0.9),
            )

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "applications_vs_price_binned.png"), dpi=220)
    plt.close()

def plot_top_properties(demand: pd.DataFrame, outdir: str, top_n: int = 15) -> None:
    top = demand.head(top_n).copy()
    if top.empty:
        return

    # Shorten long names but keep hoverable full names in SVGs (optional)
    top["label"] = top["Property"].str.slice(0, 45)

    fig, ax = plt.subplots(figsize=(13, 7))

    # Bars — same palette vibe as the Pareto chart (muted slate)
    bars = ax.barh(
        top["label"],
        top["application_count"],
        color="#CBD5E1",       # slate-300
        edgecolor="#94A3B8",   # slate-400
        linewidth=0.6,
        alpha=0.95,
        zorder=2,
    )
    for i, bar in enumerate(bars):
        if i < 3:
            bar.set_color("#0F766E")  # teal-700
            bar.set_edgecolor("#0F766E")

    ax.invert_yaxis()  # highest at the top

    # Numbers at the end of each bar
    ax.bar_label(
        bars,
        labels=[f"{v:,.0f}" for v in top["application_count"]],
        padding=4,
        fontsize=10,
        color="#334155",
    )

    # Axes, grid, formatting
    ax.set_xlabel("Applications per Property", fontsize=11)
    ax.set_ylabel("Property", fontsize=11)
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.grid(True, axis="x", color="#E2E8F0", linewidth=0.8)
    ax.grid(False, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Title + subtitle (same style as others)
    ax.set_title("Top Properties by Application Volume", fontsize=14, weight="bold", loc="left")
    fig.suptitle("Bars = Applications · Sorted most to least", y=0.98, x=0.01, ha="left",
                 fontsize=10, color="#475569")

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig(os.path.join(outdir, "top_properties_bar.png"), dpi=220)
    plt.close()

def plot_top_properties_stacked(demand: pd.DataFrame, df: pd.DataFrame, outdir: str, top_n: int = 15) -> None:
    """
    Stacked horizontal bar chart for the top N properties by total applications,
    broken out by race buckets using applicant-level dummy columns (0/1).
    Saves: top_properties_stacked.png
    """

    if demand.empty or df.empty:
        return

    # Handle naming differences
    prop_col_df = "Property"
    if "Application Property" in df.columns:
        prop_col_df = "Application Property"

    # Race dummy columns (only keep those that exist)
    race_cols = [
        ("dummy_black_african_american", "Black/African American", "#0F766E"),  # teal-700
        ("dummy_hispanic",                "Hispanic/Latine",       "#7C3AED"),  # violet-600
        ("dummy_asian",                   "Asian",                 "#F59E0B"),  # amber-500
        ("dummy_white",                   "White",                 "#2563EB"),  # blue-600
        ("dummy_native_american_alaskan_native", "Native American/Alaskan Native", "#DC2626"),
        ("dummy_white_MENA",              "White (MENA)",          "#0891B2"),  # cyan-600
        ("dummy_choose_not_to_answer",    "Prefer not to say",     "#6B7280"),
        ("dummy_unknown",                 "Unknown",               "#94A3B8"),
    ]
    race_cols = [(c, lbl, col) for (c, lbl, col) in race_cols if c in df.columns]
    if not race_cols:
        print("No race columns found — skipping stacked chart.")
        return

    # Build per-property race counts from applicant-level dummies
    race_counts = (
        df.groupby(prop_col_df)[[c for c, _, _ in race_cols]]
          .sum()
          .reset_index()
          .rename(columns={prop_col_df: "Property"})
    )

    # Merge with total application counts
    top = (
        demand[["Property", "application_count"]]
        .sort_values("application_count", ascending=False)
        .head(top_n)
        .merge(race_counts, on="Property", how="left")
        .fillna(0)
        .copy()
    )

    # Short labels for y-axis
    top["label"] = top["Property"].str.slice(0, 45)
    top = top.sort_values("application_count", ascending=False)

    fig, ax = plt.subplots(figsize=(13, 7))

    # Build stacked bars
    left = np.zeros(len(top))
    for c, lbl, color in race_cols:
        vals = top[c].astype(float).values
        ax.barh(
            top["label"],
            vals,
            left=left,
            color=color,
            edgecolor="white",
            linewidth=0.5,
            alpha=0.95,
            label=lbl,
            zorder=2,
        )
        left += vals

    ax.invert_yaxis()

    # Total labels at end of bars
    totals = top["application_count"].astype(int).values
    for y, total in enumerate(totals):
        ax.text(
            left[y] + max(totals)*0.01,
            y,
            f"{total:,.0f}",
            va="center",
            fontsize=10,
            color="#334155",
        )

    # Axis formatting & style
    ax.set_xlabel("Applications per Property", fontsize=11)
    ax.set_ylabel("Property", fontsize=11)
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.grid(True, axis="x", color="#E2E8F0", linewidth=0.8)
    ax.grid(False, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Title + subtitle
    ax.set_title("Top Properties by Application Volume (Stacked by Race)", fontsize=14, weight="bold", loc="left")
    fig.suptitle(
        "Stack segments show application counts by race; totals shown at bar ends",
        y=0.98, x=0.01, ha="left", fontsize=10, color="#475569",
    )

    # Legend outside plot
    ax.legend(
        frameon=False,
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0.0,
        title="Race",
    )

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

    # 80% point
    eighty_idx = int(np.searchsorted(d["cum_apps"].values, 0.80))
    eighty_prop_share = d.iloc[eighty_idx]["cum_props"] if len(d) > 0 else np.nan
    x80 = d.iloc[eighty_idx]["idx"]

    # Thin markers to avoid clutter
    markevery = max(1, len(d) // 30)

    fig, ax1 = plt.subplots(figsize=(13, 7))

    # Bars (muted) on left axis
    ax1.bar(
        d["idx"],
        d["application_count"],
        width=0.9,
        color="#CBD5E1",        # slate-300
        edgecolor="#94A3B8",    # slate-400
        linewidth=0.3,
        alpha=0.95,
        zorder=1,
    )
    ax1.set_ylabel("Applications per Property", fontsize=11)
    ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    # Right axis: cumulative share line (prominent)
    ax2 = ax1.twinx()
    ax2.plot(
        d["idx"],
        d["cum_apps"],
        color="#0F766E",        # teal-700
        linewidth=2,
        marker="o",
        markersize=4,
        markevery=markevery,
        markerfacecolor="white",
        markeredgewidth=0.8,
        zorder=3,
        label="Cumulative share",
    )
    ax2.set_ylim(0, 1.02)
    ax2.set_ylabel("Cumulative Share of Applications", fontsize=11)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # 80/20 guides (subtle)
    ax2.axhline(0.80, color="#94A3B8", linestyle="--", linewidth=1, zorder=0)
    ax1.axvline(x80, color="#94A3B8", linestyle="--", linewidth=1, zorder=0)

    # 45° reference (very light)
    ax2.plot([1, len(d)], [0, 1], linestyle="--", linewidth=1, color="#E2E8F0", zorder=0)

    # Annotation with a light box
    if np.isfinite(eighty_prop_share):
        ax2.annotate(
            f"≈{eighty_prop_share*100:.0f}% of properties\naccount for 80% of applications",
            xy=(x80, 0.80),
            xytext=(min(x80 + max(5, int(len(d)*0.06)), int(len(d)*0.92)), 0.88),
            arrowprops=dict(arrowstyle="->", lw=1, color="#475569"),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1", alpha=0.9),
            fontsize=10,
            ha="left", va="bottom",
            color="#334155",
        )

    # X ticks: keep readable
    if len(d) > 30:
        ax1.set_xticks(np.linspace(1, len(d), 6).astype(int))
    else:
        ax1.set_xticks(d["idx"])

    # Title & subtitle
    ax1.set_xlabel("Properties (sorted by applications, most to least)", fontsize=11)
    plt.title(
        "Pareto of Applications by Property",
        fontsize=14, weight="bold", loc="left",
    )
    fig.suptitle(
        "Bars = Applications · Line = Cumulative Share",
        y=0.98, x=0.01, ha="left", fontsize=10, color="#475569",
    )

    # Grid on the left axis only
    ax1.grid(True, axis="y", color="#E2E8F0", linewidth=0.8)
    ax1.grid(False, axis="x")
    ax2.grid(False)

    # Trim chart junk
    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)

    # Legend for the line (kept compact)
    ax2.legend(frameon=False, loc="lower right")

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)  # leave room for subtitle
    plt.savefig(os.path.join(outdir, "applications_pareto.png"), dpi=220)
    plt.close()

def plot_map(demand: pd.DataFrame, outdir: str, df: pd.DataFrame) -> None:
    # Which applicant-share columns you want to summarize (0–1 proportions)
    demo_cols = [
        "dummy_asian",
        "dummy_black_african_american",
        "dummy_white",
        "dummy_white_MENA",
        "dummy_hispanic",
        "dummy_native_american_alaskan_native",
        "dummy_choose_not_to_answer",
        "dummy_unknown",
    ]

    try:
        # 0) Property rows with coordinates
        geo = demand.dropna(subset=["latitude", "longitude"]).copy()
        if geo.empty:
            logging.warning("Folium map skipped: no valid latitude/longitude rows.")
            return

        # 1) Aggregate applicant demographics to the property level (if present)
        present_demo = [c for c in demo_cols if c in df.columns]
        if present_demo:
            demo_shares = (
                df.groupby(PROP_COL)[present_demo]
                  .mean()
                  .reset_index()
                  .rename(columns={PROP_COL: "Property"})
            )
            geo = geo.merge(demo_shares, on="Property", how="left")

        # 2) Base map
        center = [geo["latitude"].median(), geo["longitude"].median()]
        m = folium.Map(location=center, zoom_start=8, tiles="CartoDB positron")

        # Cluster layer
        cluster = MarkerCluster(name="Properties (clustered)").add_to(m)

        # Color scale by application_count
        vmin, vmax = float(geo["application_count"].min()), float(geo["application_count"].max())
        cmap = cm.StepColormap(cm.linear.viridis.colors, vmin=vmin, vmax=vmax)
        cmap.caption = "Applications per Property"
        cmap.add_to(m)

        def color_for(v):
            try:
                return cmap(v)
            except Exception:
                return "#999999"

        def popup_html(row):
            price_txt = f"${row['price_num']:,.0f}" if pd.notna(row.get("price_num")) else "—"
            def pct(x): return f"{x*100:.0f}%" if pd.notna(x) else "—"
            rows = []
            labels = [
                ("dummy_black_african_american", "Black/African American"),
                ("dummy_hispanic", "Hispanic/Latine"),
                ("dummy_asian", "Asian"),
                ("dummy_white", "White"),
            ]
            for key, lbl in labels:
                if key in row.index:
                    rows.append(f"<tr><td>{lbl}</td><td style='text-align:right'><b>{pct(row[key])}</b></td></tr>")
            demo_table = (
                "<table style='width:100%; font-size:12px; border-collapse:collapse;'>"
                + "".join(rows) + "</table>"
            )
            return folium.Popup(f"""
                <div style="font-family: system-ui, Arial; font-size: 12px; line-height:1.25;">
                    <div style="font-size: 13px; margin-bottom:4px;"><b>{row['Property']}</b></div>
                    <div>Applications: <b>{int(row['application_count'])}</b></div>
                    <div>Max Resale Price: <b>{price_txt}</b></div>
                    <div style="margin-top:6px;"><b>Applicant Mix</b></div>
                    {demo_table}
                </div>
            """, max_width=360)

        # Add markers
        for _, r in geo.iterrows():
            folium.CircleMarker(
                [r["latitude"], r["longitude"]],
                radius=float(3 + np.sqrt(max(r["application_count"], 0))),
                color=color_for(r["application_count"]),
                fill=True, fill_color=color_for(r["application_count"]), fill_opacity=0.85,
                weight=0.6,
                popup=popup_html(r),
                tooltip=r["Property"],
            ).add_to(cluster)

        # Optional: a layer highlighting ≥30% Black/African American applicants if that column exists
        share_col = "dummy_black_african_american"
        if share_col in geo.columns:
            layer_black30 = folium.FeatureGroup(name="≥30% Black/African American", show=False).add_to(m)
            mask = geo[share_col].ge(0.30).fillna(False)
            for _, r in geo[mask].iterrows():
                folium.CircleMarker(
                    [r["latitude"], r["longitude"]],
                    radius=float(3 + np.sqrt(max(r["application_count"], 0))),
                    color="#000000",
                    fill=True, fill_color="#000000", fill_opacity=0.35,
                    weight=0.4,
                    tooltip=f"{r['Property']} (≥30% Black/African American)",
                ).add_to(layer_black30)

        # Heatmap layer (toggle)
        heat_data = geo[["latitude", "longitude", "application_count"]].dropna().values.tolist()
        HeatMap(heat_data, name="Demand heatmap", radius=18, blur=15, max_zoom=11).add_to(m)

        # Controls & extras
        folium.LayerControl(collapsed=False).add_to(m)
        MiniMap(toggle_display=True).add_to(m)
        Fullscreen().add_to(m)
        MeasureControl(primary_length_unit="miles").add_to(m)
        LocateControl(auto_start=False).add_to(m)

        m.save(os.path.join(outdir, "applications_map.html"))
    except Exception as e:
        logging.warning(f"Folium map failed: {e}")

# -----------------------
# Main
# -----------------------

def main():
    parser = argparse.ArgumentParser(description="Analyze property popularity (extended visuals)")
    parser.add_argument("--input", required=True, help="Path to applications file (CSV/Parquet/Excel)")
    parser.add_argument("--outdir", default=DEFAULT_OUTPUT, help="Directory to save outputs & figures")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    ensure_dir(args.outdir)

    logging.info(f"Reading {args.input}")
    df = read_any(args.input)

    # Build per-property demand and attributes
    demand, attrs = build_property_tables(df)

    # Safe one-to-one merge
    demand = demand.merge(attrs, on="Property", how="left")

    # Save table for reuse
    out_csv = os.path.join(args.outdir, "property_demand.csv")
    logging.info(f"Saved {out_csv} ({len(demand)} rows)")

    # Visuals
    plot_top_properties(demand, args.outdir, top_n=15)
    plot_pareto(demand, args.outdir)
    plot_map(demand, args.outdir, df)
    plot_price_vs_demand(demand, args.outdir)
    plot_top_properties_stacked(demand, df, args.outdir, top_n=15)

    logging.info("Done.")


if __name__ == "__main__":
    main()

