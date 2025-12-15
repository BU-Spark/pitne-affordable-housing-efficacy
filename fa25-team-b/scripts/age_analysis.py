#!/usr/bin/env python3
"""
Age-Restricted Property Analysis

Generates visualizations analyzing age-restricted (55+/62+) affordable housing properties
and applicant demographics.

Inputs
------
--input   : data/processed/applications_clean.parquet (default)
--outdir  : output folder for visualizations (default: visuals/Age Restricted Analysis)

Outputs
-------
- age_distribution_all.png : Age distribution across all applications
- age_distribution_unique.png : Age distribution by unique applicant
- age_restricted_vs_nonrestricted.png : Age bin comparison by restriction type
- race_distribution_by_restriction_top.png : Race/ethnicity by restriction status
- applications_per_property_horizontal.png : Applications per age-restricted property
- income_by_agebin.png : Household income by age bin (log scale)
- heatmap_age_vs_race_restricted_clean.png : Age vs race heatmap for restricted properties
"""

from __future__ import annotations

import argparse
import os
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_INPUT = "data/processed/applications_clean.parquet"
DEFAULT_OUTPUT = "visuals/Age Restricted Analysis"


def load_data(input_path: str) -> pd.DataFrame:
    """Load application data from parquet file."""
    logger.info(f"Loading data from {input_path}")

    if input_path.endswith('.parquet'):
        df = pd.read_parquet(input_path)
    elif input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        raise ValueError(f"Unsupported file format: {input_path}")

    logger.info(f"Loaded {len(df)} applications")
    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare data for age analysis."""
    logger.info("Preparing data for age analysis")

    # Identify age-restricted properties
    pattern = r'\(?55\+\)?|\(?62\+\)?'
    df['age_restricted_from_property'] = df['Application Property'].str.contains(
        pattern, regex=True, na=False
    )

    # Clean and convert Age column
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

    # Create age bins
    valid_mask = df['Age'].notna()
    valid_ages = df.loc[valid_mask, 'Age'].astype(float)

    min_age = 18.0
    max_age = float(valid_ages.max()) if len(valid_ages) else 78.0
    if max_age <= min_age:
        max_age = 78.0

    bins = np.linspace(min_age, max_age, 7)
    labels = [f"{int(bins[i])}–{int(bins[i+1])}" for i in range(len(bins) - 1)]

    df['Age_bin'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True)
    df['Age_bin'] = df['Age_bin'].astype('category')
    if 'unknown' not in df['Age_bin'].cat.categories:
        df['Age_bin'] = df['Age_bin'].cat.add_categories(['unknown'])
    df['Age_bin'] = df['Age_bin'].fillna('unknown')

    logger.info(f"Age bins created: {labels + ['unknown']}")
    logger.info(f"Min age: {min_age}, Max age: {max_age}")

    return df, labels


def plot_age_distribution_all(df: pd.DataFrame, labels: list, viz_dir: str):
    """Plot age distribution across all applications."""
    logger.info("Generating age distribution (all applications)")

    plt.figure(figsize=(8, 5))
    ax = sns.countplot(
        data=df, x='Age_bin', order=labels + ['unknown'], palette='coolwarm'
    )
    plt.title('Age Distribution by Bin')
    plt.xlabel('Age Bin')
    plt.ylabel('Application Count')
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, labels=[f"{int(v.get_height())}" for v in container],
                     label_type='edge', fontsize=9, padding=3)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "age_distribution_all.png"), dpi=300)
    plt.close()


def plot_age_distribution_unique(df: pd.DataFrame, viz_dir: str):
    """Plot age distribution by unique applicant."""
    logger.info("Generating age distribution (unique applicants)")

    df_unique = df.drop_duplicates(subset='ID Number', keep='first')
    age_counts = df_unique['Age_bin'].value_counts(normalize=True).sort_index() * 100

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=age_counts.index, y=age_counts.values, palette='coolwarm')
    plt.title('Age Distribution by Unique Applicant')
    plt.xlabel('Age Bin')
    plt.ylabel('Percentage of Applicants (%)')
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, labels=[f"{v.get_height():.1f}%" for v in container],
                      label_type='edge', fontsize=9, padding=3)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "age_distribution_unique.png"), dpi=300)
    plt.close()

    return df_unique


def plot_age_restricted_comparison(df: pd.DataFrame, df_unique: pd.DataFrame, viz_dir: str):
    """Plot age-restricted vs non-age-restricted comparison."""
    logger.info("Generating age-restricted vs non-age-restricted comparison")

    age_restricted_age = (
        df_unique.groupby(['Age_bin', 'age_restricted_from_property'])['ID Number']
        .nunique().reset_index(name='applicant_count')
    )
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(
        data=age_restricted_age, x='Age_bin', y='applicant_count',
        hue='age_restricted_from_property',
        order=[c for c in df['Age_bin'].cat.categories]
    )
    plt.title('Unique Applicants by Age Bin\nAge-Restricted vs Non Age-Restricted')
    plt.xlabel('Age Bin')
    plt.ylabel('Number of Unique Applicants')
    plt.xticks(rotation=45)
    ax.legend(title='Age-Restricted Property?')
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=3, fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "age_restricted_vs_nonrestricted.png"), dpi=300)
    plt.close()


def plot_race_distribution(df_unique: pd.DataFrame, viz_dir: str):
    """Plot race distribution split by age restriction."""
    logger.info("Generating race distribution by age restriction")

    if 'race_norm_final' not in df_unique.columns:
        logger.warning("race_norm_final column not found, skipping race distribution plot")
        return

    race_counts = (
        df_unique
        .groupby(['age_restricted_from_property', 'race_norm_final'])['ID Number']
        .nunique()
        .reset_index(name='applicant_count')
    )

    overall = (
        race_counts
        .groupby('race_norm_final')['applicant_count']
        .sum()
        .sort_values(ascending=False)
    )

    top_n = 8
    top_races = overall.head(top_n).index.tolist()

    top = race_counts[race_counts['race_norm_final'].isin(top_races)].copy()
    other = race_counts[~race_counts['race_norm_final'].isin(top_races)].copy()

    if not other.empty:
        other_agg = (
            other.groupby('age_restricted_from_property')['applicant_count']
            .sum()
            .reset_index()
        )
        other_agg['race_norm_final'] = 'Other / less common'
        top = pd.concat([top, other_agg], ignore_index=True)

    top['group_total'] = top.groupby('age_restricted_from_property')['applicant_count'].transform('sum')
    top['percent'] = 100 * top['applicant_count'] / top['group_total']

    order = (
        top.groupby('race_norm_final')['applicant_count']
        .sum()
        .sort_values(ascending=False)
        .index
    )

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=top,
        y='race_norm_final',
        x='percent',
        hue='age_restricted_from_property',
        order=order,
        orient='h'
    )
    plt.title('Race/Ethnicity (Top Categories)\nAge-Restricted vs Non Age-Restricted')
    plt.xlabel('Share of Group (%)')
    plt.ylabel('Race / Ethnicity')
    ax.legend(title='Age-Restricted Property?', loc='lower right')

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "race_distribution_by_restriction_top.png"), dpi=300)
    plt.close()


def plot_applications_per_property(df: pd.DataFrame, viz_dir: str):
    """Plot applications per age-restricted property."""
    logger.info("Generating applications per age-restricted property")

    age_restricted_df = df[df['age_restricted_from_property'] == True]
    age_restricted_app_counts = (
        age_restricted_df['Application Property']
        .value_counts()
        .reset_index()
    )
    age_restricted_app_counts.columns = ['Application Property', 'application_count']

    age_restricted_app_counts['Property_label'] = (
        age_restricted_app_counts['Application Property']
        .str.replace(r'\s*\(first come, first served\)', '', regex=True)
    )

    plt.figure(figsize=(10, 4))
    ax = sns.barplot(
        data=age_restricted_app_counts,
        y='Property_label',
        x='application_count',
        orient='h'
    )
    plt.title('Applications per Age-Restricted Property')
    plt.xlabel('Number of Applications')
    plt.ylabel('Age-Restricted Property')

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=3, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "applications_per_property_horizontal.png"), dpi=300)
    plt.close()


def plot_income_by_age(df_unique: pd.DataFrame, df: pd.DataFrame, viz_dir: str):
    """Plot household income by age bin."""
    logger.info("Generating income by age bin plot")

    if 'HH Income' not in df_unique.columns:
        logger.warning("HH Income column not found, skipping income plot")
        return

    df_income = df_unique.copy()
    df_income['HH_Income_num'] = pd.to_numeric(
        df_income['HH Income'].astype(str).str.replace('[^0-9.-]', '', regex=True),
        errors='coerce'
    )
    df_income = df_income[df_income['HH_Income_num'].notna() & (df_income['HH_Income_num'] > 0)]

    plt.figure(figsize=(8, 5))
    ax = sns.boxplot(
        data=df_income, x='Age_bin', y='HH_Income_num',
        order=[c for c in df['Age_bin'].cat.categories]
    )
    plt.yscale('log')
    plt.title('Household Income (Log Scale) by Age Bin')
    plt.xlabel('Age Bin')
    plt.ylabel('Household Income (log scale)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "income_by_agebin.png"), dpi=300)
    plt.close()


def plot_age_race_heatmap(df_unique: pd.DataFrame, df: pd.DataFrame, viz_dir: str):
    """Plot age vs race heatmap for age-restricted properties."""
    logger.info("Generating age vs race heatmap")

    if 'race_norm_final' not in df_unique.columns:
        logger.warning("race_norm_final column not found, skipping heatmap")
        return

    restricted_unique = df_unique[df_unique['age_restricted_from_property'] == True].copy()

    race_counts_restricted = restricted_unique['race_norm_final'].value_counts()
    keep_races = race_counts_restricted[race_counts_restricted >= 2].index
    restricted_unique.loc[
        ~restricted_unique['race_norm_final'].isin(keep_races),
        'race_norm_final'
    ] = 'Other / less common'

    age_race_ct = (
        restricted_unique
        .groupby(['Age_bin', 'race_norm_final'])['ID Number']
        .nunique()
        .unstack(fill_value=0)
    )

    row_order = [cat for cat in df['Age_bin'].cat.categories if cat in age_race_ct.index]
    age_race_ct = age_race_ct.loc[row_order]

    col_order = age_race_ct.sum(axis=0).sort_values(ascending=False).index
    age_race_ct = age_race_ct[col_order]

    annot_data = age_race_ct.astype(str)
    annot_data[age_race_ct == 0] = ""

    plt.figure(figsize=(8, 4))
    sns.heatmap(
        age_race_ct,
        annot=annot_data,
        fmt='',
        cmap='coolwarm',
        cbar_kws={'label': 'Number of Applicants'}
    )
    plt.title('Age-Restricted Applicants\nAge Bin vs Race/Ethnicity')
    plt.xlabel('Race / Ethnicity')
    plt.ylabel('Age Bin')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "heatmap_age_vs_race_restricted_clean.png"), dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Generate age-restricted property analysis visualizations")
    parser.add_argument("--input", default=DEFAULT_INPUT, help=f"Input parquet file (default: {DEFAULT_INPUT})")
    parser.add_argument("--outdir", default=DEFAULT_OUTPUT, help=f"Output directory (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.outdir, exist_ok=True)
    logger.info(f"Output directory: {args.outdir}")

    # Load and prepare data
    df = load_data(args.input)
    df, labels = prepare_data(df)

    # Generate all visualizations
    plot_age_distribution_all(df, labels, args.outdir)
    df_unique = plot_age_distribution_unique(df, args.outdir)
    plot_age_restricted_comparison(df, df_unique, args.outdir)
    plot_race_distribution(df_unique, args.outdir)
    plot_applications_per_property(df, args.outdir)
    plot_income_by_age(df_unique, df, args.outdir)
    plot_age_race_heatmap(df_unique, df, args.outdir)

    logger.info(f"✅ All age analysis visualizations saved to {args.outdir}")


if __name__ == "__main__":
    main()
