from __future__ import annotations
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

EDITS:
    kristenbestavros - wrapped Brendan's work in a function so it can be called externally.
'''
#%% Data Import
import pandas as pd

# === ADDED: importable function wrapper ===
def normalize_current_residence(df, city_index_csv: str):
    import pandas as pd
    from rapidfuzz import process, fuzz

    # Load the city index
    df_names = pd.read_csv(city_index_csv)

    df_cleaning = df.copy()

    # --- keep their normalization rules, just point at df_cleaning ---
    states_to_remove = ["ma","ri","nh","ct","ny","massachusetts"]
    symbols = r'[,/\-]'
    direction_map = {r'\bn\b':'north', r'\bs\b':'south', r'\be\b':'east', r'\bw\b':'west'}

    # example of their replacements, keep them if present in the script
    for abbr, repl in direction_map.items():
        if "Current Residence" in df_cleaning.columns:
            df_cleaning["Current Residence"] = (
                df_cleaning["Current Residence"].astype(str)
                .str.lower()
                .str.replace(abbr, repl, regex=True)
            )

    # normalize to new column (same column name they used)
    df_cleaning["current_residence_norm_v1"] = (
        df_cleaning["Current Residence"]
        .astype(str)
        .str.split(symbols).str[0]
        .str.lower().str.strip()
        .str.replace(rf"\b({'|'.join(states_to_remove)})\b$", "", regex=True)
        .str.strip()
    )

    mass_city_list = df_names["city_manchester_manually_adjusted"].astype(str).tolist()
    mass_set = set(mass_city_list)

    NEAR_EXACT_MATCH, STRONG_MATCH, REVIEW_MATCH = 99, 95, 85
    SCORER = fuzz.WRatio

    def match_city_name(value: str):
        s = "" if pd.isna(value) else str(value).strip()
        if not s:
            return ("", 0, "empty")
        if s in mass_set:
            return (s, 100, "exact")
        candidate, score, _ = process.extractOne(s, mass_set, scorer=SCORER)
        score = int(score)
        if score >= NEAR_EXACT_MATCH:
            return (candidate, score, "near_exact_match")
        elif score >= STRONG_MATCH:
            return (candidate, score, "strong_match")
        elif score >= REVIEW_MATCH:
            return (candidate, score, "review_match")
        else:
            return (s, score, "no_MA_match")

    fuzz_output = df_cleaning["current_residence_norm_v1"].apply(match_city_name)
    df_cleaning[["matched_city","match_score","match_type"]] = (
        pd.DataFrame(fuzz_output.tolist(), index=df_cleaning.index)
    )

    return df_cleaning