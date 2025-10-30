import pandas as pd

def import_clean_HUD():

    """
    This script imports and cleans Multifamily Tax Subsidy (MTSP) Income Limit 
    data from the Housing and Urban Development (HUD) department.

    It returns a dataframe with the following columns:
        - fips code
        - hud_area_name
        - County_Name
        - county_town_name
        - variable: description for value column entry
        - value: entry matched to 'variable' description
        - HH_Size: household size matched with value and description columns

    This dataset is matchable to other geographic data via county or FIPS code. 
    """
    dt = pd.read_excel("https://www.huduser.gov/portal/datasets/mtsp/mtsp25/MTSP-Data-FY25.xlsx")

    # filtering only MA -- might need to include other regions in future
    dt = dt[dt["stusps"] == "MA"].reset_index(drop=True)

    # filtering columns
    dt = dt[['fips', 'hud_area_name', 'County_Name', 'county_town_name', 
             'median2025', 'lim50_25p1', 'lim50_25p2', 'lim50_25p3', 'lim50_25p4', 
             'lim50_25p5', 'lim50_25p6', 'lim50_25p7', 'lim50_25p8']]
    
    # melting dataframe
    dt = dt.melt(id_vars = ['fips', 'hud_area_name', 'County_Name', 'county_town_name'])

    # adding new column, 'HH_Size', for household-dependent numbers
    dt["HH_Size"] = dt["variable"].str.extract(r"p([1-8])$")[0].astype(float)

    return dt
