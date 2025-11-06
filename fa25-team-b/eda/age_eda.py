# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:49:21 2025

@author: Brendan and Aadi 
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%% Setup: Output folder
viz_dir = "visualizations"
os.makedirs(viz_dir, exist_ok=True)

#%% Load Data and Clean Columns
df = pd.read_excel("CHAPA Chapter 40B Application Data_Oct 2023 to May 2025 - Confidential.xlsx")

df.columns = df.columns.str.strip().str.replace("\n", " ").str.replace("  ", " ")

rename_map = {
    "Race/Ethnicity": "race_norm_final",
    "Applicant ID": "ID Number",
    "Property Applied For": "Application Property",
    "Household Income": "HH Income",
    "Household Assets": "HH Assets",
    "First Time Homebuyer Class": "FTHB Class?",
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# noticed naming convention was yielding this as two separate properties
df['Application Property'] = df['Application Property'].astype(str).str.replace(
    '110 Dillingham Ave, Unit 105 ~ Falmouth (62+)... (first come, first served)',
    '110 Dillingham Ave, Unit 105 ~ Falmouth (62+) (first come, first served)',
    regex=False
)

#%% Identify Age-Restricted Properties

pattern = r'\(?55\+\)?|\(?62\+\)?'
age_restricted_df = df[df['Application Property'].str.contains(pattern, regex=True, na=False)]
df['age_restricted_from_property'] = df['Application Property'].str.contains(pattern, regex=True, na=False)

unique_restricted_homes = age_restricted_df['Application Property'].unique()
unique_id_for_restricted_homes = age_restricted_df['ID Number'].unique()

unique_id_count_restricted_homes = age_restricted_df['ID Number'].value_counts().reset_index()
unique_id_count_restricted_homes.columns = ['id_number', 'restricted_application_count']

#%% Age Columns Setup

age_cols = [
    'ID Number', 'Submission Date', 'Application Property', 'Source', 'Age',
    'race_norm_final', 'Disability', 'Current Residence', 'HH Size',
    'Dependents', 'HH Type', 'HH Income', 'HH Assets', 'FTHB Class?'
]
df_ages = df[age_cols]

count_missing_age_by_id = (
    df_ages.groupby('ID Number')['Age']
    .apply(lambda x: x.isna().sum())
    .reset_index(name='missing_age_count')
)

#%% Clean and Bin Age

df['Age'] = (
    df['Age']
    .replace('u/a', pd.NA)
    .astype('string')
)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

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

print(f"Min valid age used for binning: {min_age}")
print(f"Max valid age used for binning: {max_age}")
print("\nBin counts:")
print(df['Age_bin'].value_counts().sort_index())

#%% Visualization 1: Age Distribution

plt.figure(figsize=(8,5))
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
plt.show()

#%% Visualization 2: Age Distribution by Unique Applicant

df_unique = df.drop_duplicates(subset='ID Number', keep='first')
age_counts = df_unique['Age_bin'].value_counts(normalize=True).sort_index() * 100

plt.figure(figsize=(8,5))
ax2 = sns.barplot(x=age_counts.index, y=age_counts.values, palette='coolwarm')
plt.title('Age Distribution by Unique Applicant')
plt.xlabel('Age Bin')
plt.ylabel('Percentage of Applicants (%)')
plt.xticks(rotation=45)
for container in ax2.containers:
    ax2.bar_label(container, labels=[f"{v.get_height():.1f}%" for v in container],
                  label_type='edge', fontsize=9, padding=3)
plt.tight_layout()
plt.savefig(os.path.join(viz_dir, "age_distribution_unique.png"), dpi=300)
plt.show()

#%% Dataset Overview and Inspection

print("\n Dataset Overview")
print(f"Shape: {df.shape}")
print("\nColumn Names:")
print(df.columns.tolist())
print("\nMissing values by column:")
print(df.isna().sum().sort_values(ascending=False).head(15))
print("\nSample rows:")
print(df.head(3))
print("\nUnique values in 'Application Property':")
print(df['Application Property'].dropna().unique()[:10])
if 'race_norm_final' in df.columns:
    print("\nUnique Race/Ethnicity values:")
    print(df['race_norm_final'].dropna().unique()[:10])

#%% ===================== ADDITIONAL VISUALIZATIONS =====================

# 1) Applicants by Age Bin vs Age-Restricted Flag
age_restricted_age = (
    df_unique.groupby(['Age_bin','age_restricted_from_property'])['ID Number']
    .nunique().reset_index(name='applicant_count')
)
plt.figure(figsize=(8,5))
ax = sns.barplot(
    data=age_restricted_age, x='Age_bin', y='applicant_count',
    hue='age_restricted_from_property',
    order=[c for c in df['Age_bin'].cat.categories]
)
plt.title('Unique Applicants by Age Bin\nAge-Restricted vs Non Age-Restricted')
plt.xlabel('Age Bin'); plt.ylabel('Number of Unique Applicants')
plt.xticks(rotation=45); ax.legend(title='Age-Restricted Property?')
for container in ax.containers:
    ax.bar_label(container, fmt='%d', padding=3, fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(viz_dir, "age_restricted_vs_nonrestricted.png"), dpi=300)
plt.show()

# 2) Race Distribution Split by Age Restriction (cleaned up)
if 'race_norm_final' in df_unique.columns:
    # base counts
    race_counts = (
        df_unique
        .groupby(['age_restricted_from_property', 'race_norm_final'])['ID Number']
        .nunique()
        .reset_index(name='applicant_count')
    )

    # overall frequency across both groups
    overall = (
        race_counts
        .groupby('race_norm_final')['applicant_count']
        .sum()
        .sort_values(ascending=False)
    )

    top_n = 8  # number of named categories to keep
    top_races = overall.head(top_n).index.tolist()

    # split into top and "other"
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

    # recompute group-wise percentages
    top['group_total'] = top.groupby('age_restricted_from_property')['applicant_count'].transform('sum')
    top['percent'] = 100 * top['applicant_count'] / top['group_total']

    # order categories by overall size
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
    plt.show()


# 3) Applications per Age-Restricted Property
# 3) Applications per Age-Restricted Property (horizontal, cleaner labels)
age_restricted_app_counts = (
    age_restricted_df['Application Property']
    .value_counts()
    .reset_index()
)
age_restricted_app_counts.columns = ['Application Property', 'application_count']

# optional: slightly shorter label for plotting
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
plt.show()


# 4) Household Income by Age Bin (Log Scale)
if 'HH Income' in df_unique.columns:
    df_income = df_unique.copy()
    df_income['HH_Income_num'] = pd.to_numeric(
        df_income['HH Income'].astype(str).str.replace('[^0-9.-]', '', regex=True),
        errors='coerce'
    )
    df_income = df_income[df_income['HH_Income_num'].notna() & (df_income['HH_Income_num'] > 0)]
    plt.figure(figsize=(8,5))
    ax = sns.boxplot(
        data=df_income, x='Age_bin', y='HH_Income_num',
        order=[c for c in df['Age_bin'].cat.categories]
    )
    plt.yscale('log')
    plt.title('Household Income (Log Scale) by Age Bin')
    plt.xlabel('Age Bin'); plt.ylabel('Household Income (log scale)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "income_by_agebin.png"), dpi=300)
    plt.show()

# 5) Heatmap: Age Bin vs Race (Age-Restricted Only, cleaned + compact)
if 'race_norm_final' in df_unique.columns:
    # work only with age-restricted, unique applicants
    restricted_unique = df_unique[df_unique['age_restricted_from_property'] == True].copy()

    # collapse rare races into "Other / less common" to keep plot readable
    race_counts_restricted = restricted_unique['race_norm_final'].value_counts()
    keep_races = race_counts_restricted[race_counts_restricted >= 2].index  # threshold can be 2 or 3
    restricted_unique.loc[
        ~restricted_unique['race_norm_final'].isin(keep_races),
        'race_norm_final'
    ] = 'Other / less common'

    # crosstab: Age_bin x race
    age_race_ct = (
        restricted_unique
        .groupby(['Age_bin', 'race_norm_final'])['ID Number']
        .nunique()
        .unstack(fill_value=0)
    )

    # order rows by the original age-bin category order
    row_order = [cat for cat in df['Age_bin'].cat.categories if cat in age_race_ct.index]
    age_race_ct = age_race_ct.loc[row_order]

    # order columns by total counts (most common races first)
    col_order = age_race_ct.sum(axis=0).sort_values(ascending=False).index
    age_race_ct = age_race_ct[col_order]

    # annotate only non-zero cells
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
    plt.show()
