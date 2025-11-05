# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:49:21 2025

@author: Brendan and Aadi 
"""

import pandas as pd

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
        regex=False # needs to be false due to the ... present in the entry
    )

pattern = r'\(?55\+\)?|\(?62\+\)?'

age_restricted_df = df[df['Application Property'].str.contains(pattern, regex=True, na=False)]


df['age_restricted_from_property'] = df['Application Property'].str.contains(pattern, regex=True, na=False)

# returns 6 properties with 55+ or 62+ in the 'Application Property' Columns
unique_restricted_homes = age_restricted_df['Application Property'].unique()

# returns 31 different applicants for the 6 unique properties
unique_id_for_restricted_homes = age_restricted_df['ID Number'].unique()

# returns 4 applicants applied for 2 restricted properties, the other 27 applied to only one
unique_id_count_restricted_homes = age_restricted_df['ID Number'].value_counts().reset_index()
unique_id_count_restricted_homes.columns = ['id_number', 'restricted_application_count']

#%% Age Columns

# u/a = underage? remove?
# 0.0 remove?

age_cols = cols_cleaning = [
    'ID Number', 'Submission Date',
    'Application Property', 'Source',
    'Age', 'race_norm_final', 'Disability',
    'Current Residence', 'HH Size',
    'Dependents', 'HH Type', 'HH Income',
    'HH Assets', 'FTHB Class?'
]

df_ages = df[age_cols]

'''
ID Number                 int64
Submission Date          object
Application Property     object
Source                   object
Age                      object
race_norm_final          object
Disability               object
Current Residence        object
HH Size                   int64
Dependents              float64
HH Type                  object
HH Income                object
HH Assets                object
FTHB Class?              object
dtype: object
'''

# start by finding null or string entries and convert all to numeric (no decimals)

# 112 total NA ages
count_missing_age_by_id = (
    df_ages.groupby('ID Number')['Age']
    .apply(lambda x: x.isna().sum())
    .reset_index(name='missing_age_count')
)

#%%

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1) Clean raw age -> keep numeric in df['Age']
df['Age'] = (
    df['Age']
    .replace('u/a', pd.NA)    
    .astype('string')
)

df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # Float64 with <NA>

# 2) Build bins only from valid numeric ages
valid_mask = df['Age'].notna()
valid_ages = df.loc[valid_mask, 'Age'].astype(float)

# Guard if data is sparse
min_age = 18.0
max_age = float(valid_ages.max()) if len(valid_ages) else 78.0
if max_age <= min_age:
    max_age = 78.0

bins = np.linspace(min_age, max_age, 7)  # 6 bins
labels = [f"{int(bins[i])}–{int(bins[i+1])}" for i in range(len(bins) - 1)]

# 3) Create Age_bin directly; add 'unknown' category
df['Age_bin'] = pd.cut(
    df['Age'], bins=bins, labels=labels, include_lowest=True
)  # result is categorical with NaN for missing ages

df['Age_bin'] = df['Age_bin'].astype('category')
if 'unknown' not in df['Age_bin'].cat.categories:
    df['Age_bin'] = df['Age_bin'].cat.add_categories(['unknown'])
df['Age_bin'] = df['Age_bin'].fillna('unknown')

# 4) Integrity print
print(f"Min valid age used for binning: {min_age}")
print(f"Max valid age used for binning: {max_age}")
print("\nBin counts:")
print(df['Age_bin'].value_counts().sort_index())


plt.figure(figsize=(8,5))
ax = sns.countplot(
    data=df,
    x='Age_bin',
    order=labels + ['unknown'],
    palette='coolwarm'
)
plt.title('Age Distribution by Bin')
plt.xlabel('Age Bin')
plt.ylabel('Application Count')
plt.xticks(rotation=45)

# Add count labels on top of each bar
for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"{int(v.get_height())}" for v in container],
        label_type='edge',
        fontsize=9,
        padding=3
    )

plt.tight_layout()
plt.show()

df_unique = df.drop_duplicates(subset='ID Number', keep='first')

age_counts = df_unique['Age_bin'].value_counts(normalize=True).sort_index() * 100

print("Age Distribution by Unique Applicant (%):")
print(age_counts.round(2))

plt.figure(figsize=(8,5))
ax2 = sns.barplot(
    x=age_counts.index,
    y=age_counts.values,
    palette='coolwarm'
)
plt.title('Age Distribution by Unique Applicant')
plt.xlabel('Age Bin')
plt.ylabel('Percentage of Applicants (%)')
plt.xticks(rotation=45)

# Add percentage labels on each bar
for container in ax2.containers:
    ax2.bar_label(
        container,
        labels=[f"{v.get_height():.1f}%" for v in container],
        label_type='edge',
        fontsize=9,
        padding=3
    )

plt.tight_layout()
plt.show()

print("\n Dataset Overview")
print(f"Shape: {df.shape}")
print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing values by column:")
print(df.isna().sum().sort_values(ascending=False).head(15))

print("\nSample rows:")
print(df.head(3))

print("\nUnique values in 'Application Property' (check naming consistency):")
print(df['Application Property'].dropna().unique()[:10])

print("\nUnique values in 'Race/Ethnicity' or renamed 'race_norm_final':")
if 'race_norm_final' in df.columns:
    print(df['race_norm_final'].dropna().unique()[:10])
