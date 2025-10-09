# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 19:35:04 2025

@author: brend
"""

import pandas as pd
import re

df = pd.read_csv('df_cleaning_v1.csv')

#%% Ethnicity Naming Normalization

''' Application Demographic Options
Asian/Pacific Islander
Black or African American # will be using black/african american for now
Native American/Alaskan Native
White/Non-Minority
Hispanic/Latino
Other Race/Ethnicity (please specify)
Disabled
Senior Citizen
Veteran
'''

original_race_counts = df['Race/Ethnicity'].value_counts() # starts with 99 unique race entries

CANDIDATE_COL = 'Race/Ethnicity'

#%% Ethnicity norm v1

df['race_norm_v1'] = (
    df['Race/Ethnicity']
    .astype(str)
    .str.lower()
    .str.strip()
)

# deals with any missing/null values
df['race_norm_v1']  = (
    df['race_norm_v1'].mask
    (df['race_norm_v1'].isin(['nan','NaN', 'none', 'null', ''])
    ))

df['race_norm_v1'] = (
    df['race_norm_v1']
    .str.normalize('NFKD') # breaks apart any special characters
    .str.encode('ascii', 'ignore') # removes any extra characters just created in the previous line
    .str.decode('utf-8') # converts back to standard strings
)

df['race_norm_v1'] = (
    df['race_norm_v1']
    .str.replace(
        r'\s+', ' ', regex=True # replaces any regex characters with a standard space (' ')
    ))

unique_race_counts_v1 = df['race_norm_v1'].value_counts() # 99 to 83 different race entries
unique_race = df['race_norm_v1'].unique()
# print(unique_race)

df['race_norm_v1'] = (
    df['race_norm_v1']
    .str.replace(r'[\"]', '', regex=True)
)

# removes all symbols except: separated by | symbol
    # a-z | 0-9 | whitespace (\s) | , | / | & | - |
df['race_norm_v1'] = (
    df['race_norm_v1']
    .str.replace(r'[^a-z0-9\s,/&-]', '', regex=True)
)
# confirms no new whitespace is created, if it is, removes it
df['race_norm_v1'] = (
    df['race_norm_v1']
    .str.replace(
        r'\s+', ' ', regex=True
    ).str.strip()
)
# one less race option (82) now

#%% Ethnicity norm v2
# ensure commas, black-slashes, and '&' characters conventions are normalized

# \s means any whitespace, * means 0 or more
# this ensures all instances are found for each entry, if multiple exist
df['race_norm_v1'] = (
    df['race_norm_v1']
    .str.replace(r'\s*,\s*', ', ', regex=True) # replaces instances with ', '
    .str.replace(r'\s*/\s*', '/', regex=True) # replaces instances with '/'
    .str.replace(r'\s*&\s*', ' & ', regex=True) # replaces instances with ' & '
    .str.replace(r'\s+or\s+', '/', regex=True) # replaces instances of 'or' with '/'
)

# down to 83 races

df['race_norm_v2'] = (
    df['race_norm_v1']
    .str.replace(r'\s*,\s*', '/', regex=True) # replaces instances with ', '
    .str.replace(r'\s*/\s*', '/', regex=True) # replaces instances with '/'
    .str.replace(r'\s*&\s*', '/', regex=True) # replaces instances with ' & '
    .str.replace(r'\s+or\s+', '/', regex=True) # replaces instances of 'or' with '/'
)

# down to 80 races
unique_race_v2 = df['race_norm_v2'].unique()
#%% Unknowns Cleaning

convert_to_unknown = [
    'unknown', 'nan', 'other', 'did not list',
    'choose not to answer', 'choose not to answer/'
]    

df['race_norm_v2'] = (
    df['race_norm_v2']
    .replace(convert_to_unknown, 'unknown')
)
# down to 76 races after removal of unknowns

#%% African American Cleaning NEEDS TO BE CORRECTED

black_unique = (
    df['race_norm_v2']
    .dropna()
    .astype(str)
    .unique()
)

black_unique = [a for a in black_unique if 'black' in a]
print(black_unique)

convert_to_black = [
    'black/afr am',
    'black/af am',
    'african/amer',
    'black/afr amer',
    'afr amer',
    'cape vrd blck',
    'african amer',
    'black/african american',
    'black'
    ]

black_ordering = sorted(set(convert_to_black), key=len, reverse=True)
black_pattern = '|'.join(re.escape(a) for a in black_ordering)

df['race_norm_v2'] = (
    df['race_norm_v2']
    .astype(str)
    .replace(black_pattern, 'black_african_american', regex=True)
)

unique_race_v2 = df['race_norm_v2'].unique() # down to 69 races after black/african american normalization

black_unique_cleaned = (
    df['race_norm_v2']
    .dropna()
    .astype(str)
    .unique()
)

black_unique_cleaned = [a for a in black_unique_cleaned if 'black' in a]
#%% Hispanic/Latino Cleaning

# starting with 21 unique entries containing hispanic
hispanic_unique = (
    df['race_norm_v2']
    .dropna()
    .astype(str)
    .unique()
)

hispanic_unique = [a for a in hispanic_unique if 'hispanic' in a]
print(hispanic_unique)

convert_to_hispanic = [
     'hispanic hispanic', 'hispanic/latino hispanic/latino',
    'hispanic hispanic/latino', 'latino hispanic/latino',
    'hispanic latino hispanic/latino', 'brazilian hispanic/latino',
    'spanish hispanic/latino', 'guatemalan hispanic/latino',
    'latin american hispanic/latino', 'latino hispanic/latino',
    'part south american indian guarani tribe hispanic/latino',
    '/hispanic', 'hispanic/latino'
]    
hispanic_ordering = sorted(set(convert_to_hispanic), key=len, reverse=True)
hispanic_pattern = '|'.join(re.escape(h) for h in hispanic_ordering)

df['race_norm_v3'] = (
    df['race_norm_v2']
    .str
    .replace(hispanic_pattern, 'hispanic', regex=True)
)

hispanic_unique_v3 = (
    df['race_norm_v3']
    .dropna()
    .astype(str)
    .unique()
)
hispanic_unique_v3 = [a for a in hispanic_unique_v3 if 'hispanic' in a]
print(len(hispanic_unique_v3)) # down to 11 options containing 'hispanic'

unique_race_v3 = df['race_norm_v3'].unique() # down to 57 race options

#%% Native American & Alaskan Native Naming Conventions 
# 9 options containing 'native'
native_american_unique = [
    n for n in unique_race_v3 if isinstance(n, str) and 'native' in n]

df['race_norm_v4'] = (
    df['race_norm_v3']
    .astype(str)
    .str.replace('cherokee native american', 'native_american_alaskan_native', regex=True)
    .str.replace('native amer/alaskan', 'native_american_alaskan_native', regex=True)
    .str.replace('native american/alaskan native', 'native_american_alaskan_native', regex=True)
    .str.replace('native american', 'native_american_alaskan_native', regex=True)
)

unique_race_v4 = df['race_norm_v4'].unique() # down to 55 race selections 
  
# down to 5 options for Native American/Alaskan Native
native_american_unique_post_clean = [
    n for n in unique_race_v4 if isinstance(n, str) and 'native_american' in n]

print(unique_race_v4)
#%% Asian Naming Conventions CONFIRM 'asian pacific islander/native hawaiian' COUNTS

# 11 unique entries
asian_unique = [
    n for n in unique_race_v4 if isinstance(n, str) and 'asian' in n]

convert_to_asian = [
    'asian', 'south asian pakistai', 'asian/pacific islander',
    'asian pacific islander/native hawaiian', 'asian kazakh' 
    
    ]    
asian_ordering = sorted(set(convert_to_asian), key=len, reverse=True)
asian_pattern = '|'.join(re.escape(h) for h in asian_ordering)

df['race_norm_v5'] = (
    df['race_norm_v4']
    .str
    .replace(asian_pattern, 'asian_pacific_islander', regex=True)
)

#%% White Naming Conventions (white & some white_MENA)

# 21 unique entries
white_unique = [
    n for n in unique_race_v4 if isinstance(n, str) and 'white' in n]

# full white, then white MENA subcategory later on

df['race_norm_v5'] = (
    df['race_norm_v5']
    .str
    .replace(r'/$', '', regex=True) # converts the 'white/' entry to 'white'
)

df['race_norm_v5'] = (
    df['race_norm_v5']
    .astype(str)
    .str.replace('white-north african', 'white_MENA', regex=True)
    .str.replace('white/lebanese/syrian', 'white_MENA', regex=True)
    .str.replace('whitehispanic', 'white/hispanic', regex=True)
    .str.replace('white hispanic', 'white/hispanic', regex=True)
    .str.replace('middle eastern/north african white', 'white_MENA', regex=True)
)


unique_race_v5 = df['race_norm_v5'].unique() # 46 races
  
# down to 16 options containing white
white_unique_post_clean = [
    n for n in unique_race_v5 if isinstance(n, str) and 'white' in n]


#%% MENA Replacements

convert_to_white_MENA = [
    'north african', 'egyptian', 'middle eastern',
    'iraqi-american', 'afghan', 
    'middle eastern/north african',
    ]    
white_MENA_ordering = sorted(set(convert_to_white_MENA), key=len, reverse=True)
white_MENA_pattern = '|'.join(re.escape(h) for h in white_MENA_ordering)

df['race_norm_v5'] = (
    df['race_norm_v5']
    .str
    .replace(white_MENA_pattern, 'white_MENA', regex=True)
)

df['race_norm_v5'] = (
    df['race_norm_v5']
    .astype(str)
    .str.replace('nan', 'unknown', regex=True)
    .str.replace('nl', 'unknown', regex=True)
    .str.replace('wihite', 'white', regex=True)
    .str.replace('choose not to answerhispanic/latino', 'choose not to answer/hispanic', regex=True)
)

unique_race_v5 = df['race_norm_v5'].unique() # 36 race options

#%% Specific Case Replacements (Final Normalized Form)

df['race_norm_v6'] = (
    df['race_norm_v5']
    .astype(str)
    .str.replace('black_african_american hispanic', 'black_african_american/hispanic', regex=True)
    .str.replace('cape verde portuguese', 'hispanic', regex=True)
    .str.replace('cape verdean', 'black_african_american/hispanic', regex=True)
    .str.replace('south asia - pakistan', 'asian', regex=True)
    .str.replace('pakistani/ukrainian', 'asian/white', regex=True)
    .str.replace('uyghur', 'asian', regex=True)
    .str.replace('pacific islander/native hawaiian', 'asian', regex=True)
    .str.replace('asian_pacific_islander', 'asian', regex=True)
    .str.replace('italian', 'white', regex=True)
    .str.replace('greek', 'white', regex=True)
    .str.replace('brazilian', 'hispanic', regex=True)
    
)

unique_race_v6 = df['race_norm_v6'].unique() # 27 combos
print(unique_race_v6.tolist())

df['race_norm_v6'] = (
    df['race_norm_v6']
    .astype(str)
    .str.replace('choose not to answer/hispanic', 'choose_not_to_answer/hispanic', regex=True)
    .str.replace('asian black_african_american white_MENA','asian/black_african_american/white_MENA', regex=True)
    .str.replace('black_african_american white','black_african_american/white', regex=True)
    .str.replace('european/african', 'white/black_african_american', regex=True)
)
unique_race_v6 = df['race_norm_v6'].unique() # 25 combos

# european/african = ?

df['race_norm_final'] =  (
    df['race_norm_v6']
    .astype(str)
    .str.replace(' ', '/', regex=True)
)

unique_race_final = df['race_norm_final'].unique() # 22 combos

#%% Race Splits & Dummy Variables

race_name_map = [
    'asian',
    'black_african_american',
    'native_american_alaskan_native',
    'white',
    'white_MENA',
    'hispanic', # changed to hispanic so I do not have to worry about slash in 'hispanic/latino'
    'choose_not_to_answer',
    'unknown' # added temporarily
]

for race in race_name_map:
    df[f'dummy_{race}'] = (
        df['race_norm_final']
        .str.contains(race, regex=False).astype(int)
    )
df['is_mixed_race'] = df[[f'dummy_{race}' for race in race_name_map]].sum(axis=1).gt(1).astype(int)

race_cleaning_process_df = df[
    ['ID Number', 'Race/Ethnicity',
     'race_norm_v1', 'race_norm_v2',
     'race_norm_v3', 'race_norm_v4',
     'race_norm_v5', 'race_norm_v6',
     'race_norm_final'
     ]]

# race_cleaning_process_df.to_csv('race_normalization_iterations.csv')


df_clean = df.copy()
df_clean = (
    df_clean.drop(
        columns=['race_norm_v1', 'race_norm_v2', 'race_norm_v3',
                 'race_norm_v4', 'race_norm_v5','race_norm_v6'
                 ]
        ))

#%%

