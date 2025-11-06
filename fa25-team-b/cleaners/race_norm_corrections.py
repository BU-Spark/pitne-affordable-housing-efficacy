# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 15:09:28 2025

@author: brend
"""

import pandas as pd

df = pd.read_csv("Applications_with_Resale_Data_main.csv")

race_name_map = [
    'asian',
    'black_african_american',
    'native_american_alaskan_native',
    'white',
    'white_MENA',
    'hispanic',
    'choose_not_to_answer', # will be removed later
    'unknown'
]

#%% Original Counts

dummy_cols = [col for col in df.columns if col.startswith('dummy_')]
dummy_cols_and_mixed_col = dummy_cols + ['is_mixed_race']

print(df[dummy_cols_and_mixed_col].sum())

'''
dummy_asian                             231
dummy_black_african_american            277
dummy_native_american_alaskan_native     11
dummy_white                             983
dummy_white_MENA                         51
dummy_hispanic                          254
dummy_choose_not_to_answer                6
dummy_unknown                            80
is_mixed_race                           144
dtype: int64

'''
#%%

def CNTA_hispanic_correction(df, col):
    ''' DocString
    Parameters
    ----------
    df : pd.DataFrame
        Any CHAPA df with race columns
    col : str, default is 'race_norm_final'
        Any column that needs to replace 'choose_not_to_answer/hispanic' with 'hispanic'

    Returns
    -------
    Returns original df, with modifed entries in the column selected

    '''
    df[col] = (
        df[col]
        .astype(str) # regex = False, exact matches only
        .str.replace('choose_not_to_answer/hispanic', 'hispanic', regex=False)
)
    return df
# adjust column name when calling the function if needed
df = CNTA_hispanic_correction(df, col='race_norm_final')


# corrects issue of classifying white_MENA as mixed race
def update_dummy_cols(df, col, race_name_map):
    ''' DocString
    Parameters
    ----------
    df : pd.DataFrame
        Any CHAPA df that contains dummy cols and 'is_mixed_race' col
    col : str
        Full race name column being used (ex. 'race_norm_final')
    race_name_map : list
        List of all races with dummy variables created
        'dummy_' + {race_list_entry}, ex. (ex. 'dummy_white_MENA')

    Returns
    -------
    Returns original df, with modifed dummy cols and 'is_mixed_race' col
    '''
    for race in race_name_map:
        dummy_col = f'dummy_{race}'
        if dummy_col in df.columns:
            df[dummy_col] = (
                df[col]
                .astype(str)
                .str.split('/')
                .apply(lambda x: int(race in x if isinstance(x, list) else False))
        )
    
    df['is_mixed_race'] = (
        df[[f'dummy_{race}' for race in race_name_map if f'dummy_{race}' in df.columns]]
        .sum(axis=1)
        .gt(1)
        .astype(int)
    )

    return df

# adjust column name when calling the function if needed
df = update_dummy_cols(df, col='race_norm_final', race_name_map=race_name_map)

#%% Data Integrity Check

def race_dummies_sums(df):
    ''' DocString
    Summarizes the total counts for all dummy race cols 
    and the 'is_mixed_race' col

    Parameters
    ----------
    df : pd.DataFrame
        The df containing dummy race cols

    Returns
    -------
    pd.Series
        Sum of each dummy col and 'is_mixed_race' col
'''

    dummy_cols = [col for col in df.columns if col.startswith('dummy_')]
    dummy_cols_and_mixed_col = dummy_cols + ['is_mixed_race']
    summary = df[dummy_cols_and_mixed_col].sum()
    print(summary)
    return summary

summary = race_dummies_sums(df)

