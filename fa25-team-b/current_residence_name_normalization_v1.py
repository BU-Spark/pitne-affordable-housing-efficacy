# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 17:19:04 2025

@author: brend
"""

'''
Data Cleaning goals:
    confirm the symbols split does not mess anything up Ex. a city called O'Neal
    need to deal with east/west, north/south, etc.
    normalize abbreviations:  n. s. e. w. as full words
    decide to combine regions, ex. East Boston, West Boston, and Boston as just Boston
Sources:
    https://www.mass.gov/files/csv/2024-07/City_and_Town_Clerks.csv

'''
#%% Data Import

import pandas as pd

df = pd.read_csv('CHAPA_applications_concat_unclean.csv')
df_names = pd.read_csv('city_names_norm_ma.csv')

# 350 MA city names, use as fuzzy match index
df_mass_city_index = df_names['city_manchester_manually_adjusted']

#%% Applicant Grouping/Frequency Counts

id_num_grouping = df.groupby('ID Number').size().reset_index(name='count')
id_num_grouping['num_unqiue_id'] = df['ID Number'].nunique() # confirms number of unique applicants is 1,299

id_num_grouping['id_sum'] = id_num_grouping['count'].sum() # confirms total applications is 1,740

# number of id_numbers group by count of applications submitted (using id_num as pk)
freq_counts = id_num_grouping['count'].value_counts().reset_index()
freq_counts = freq_counts.rename(columns={'index':'num_applications', 'count':'id_count'})

#%% Initial Cleaning

df_cleaning = df.copy() # copies the original df

states_to_remove = ["ma", "ri", "nh", "ct", "ny", 'massachusetts'] # states to split current_residence on
symbols = r'[,/\-]' # list of potential symbols to split current_residence on
direction_map = {
    r'\bn\b':'north', r'\bn\.b':'north',    
    r'\bs\b':'south', r'\bs\.b':'south',
    r'\be\b':'east', r'\be\.b':'east',
    r'\bw\b':'west', r'\bw\.b':'west'
}

for abbreviation, replacement in direction_map.items():
    df_cleaning['Current Residence'] = (
        df_cleaning['Current Residence']
        .str.lower()
        .str.replace(abbreviation, replacement, regex=True)
    )

df_cleaning['current_residence_norm_v1'] = (
    df['Current Residence']
    .str
    .split(symbols).str[0] # first split on symbol, only take leftmost part
    .str.lower().str.strip() # convert to lowercase and trim
     #rf = raw string, bf = word boundary
    .str.replace(rf"\b({'|'.join(states_to_remove)})\b$", "", regex=True)
    .str.strip()
)

#%% Naming Conventions and Fuzzy Match

from rapidfuzz import process, fuzz

mass_city_list = df_mass_city_index.tolist()
mass_set = set(mass_city_list)

# --- Configuration ---
candidate_col = 'current_residence_norm_v1'

NEAR_EXACT_MATCH = 99
STRONG_MATCH = 95
REVIEW_MATCH = 85

SCORER = fuzz.WRatio

results_map = {}

# --- Matching ---
def match_city_name(value: str):
    s = '' if pd.isna(value) else str(value).strip()
    
    if not s:
        return ('', 0, 'empty')
    
    if s in mass_set:
        return (s, 100, 'exact')
    
    candidate, score, _ = process.extractOne(s, mass_set, scorer=SCORER)
    if score >= NEAR_EXACT_MATCH:
        return (candidate, int(score), 'near_exact_match')
    elif score >= STRONG_MATCH:
        return (candidate, int(score), 'strong_match')
    elif score >= REVIEW_MATCH:
        return (candidate, int(score), 'review_match')
    else:
        return (s, int(score), 'no_MA_match')
    
fuzz_output = df_cleaning['current_residence_norm_v1'].apply(match_city_name)
df_cleaning[['matched_city', 'match_score', 'match_type']] = (
    pd.DataFrame(fuzz_output.tolist(),index=df_cleaning.index)
    )

id_matched_df = df_cleaning[['ID Number', 'current_residence_norm_v1', 'matched_city', 'match_score', 'match_type']]

fuzz_type_counts = (
    id_matched_df['match_type'].value_counts()
)

'''fuzzy matching results
1501 exact matches
136 cities not found in MA city list
5 cities > 95 fuzzy match score
93 cities > 85 fuzzy match score
5 cities empty

'''

