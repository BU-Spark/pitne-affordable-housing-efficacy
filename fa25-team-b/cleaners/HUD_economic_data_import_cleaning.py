from __future__ import annotations
import pandas as pd

def import_clean_append_HUD(app_df: pd.DataFrame):

    """
    This script imports, cleans, and appends Multifamily Tax Subsidy (MTSP) Income Limit 
    data from the Housing and Urban Development (HUD) department to applicant data.

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

    # creating a 'city' column that matches 'matched city' column in applicant dataset
    dt['city'] = (
        dt["county_town_name"]
        .str.replace(r"\s*(town|city)\b", "", case=False, regex=True)
        .str.lower()
        .str.strip()
    )

    # Merging to applicant dataset
    merged = app_df.merge(
        dt[["HH_Size", "city", "value"]],
        left_on=["HH Size", "matched_city"],
        right_on=["HH_Size", "city"],
        how="left"
    )

    # Handle NA rows by imputing median values for location (without HH_Size)
    mask_missing = merged["value"].isna()
    fallback = app_df.merge(
        dt.loc[dt["variable"] == "median2025", ["city", "value"]],
        left_on="matched_city",
        right_on="city",
        how="left"
    )

    # combining two merges
    merged.loc[mask_missing, "value"] = fallback.loc[mask_missing, "value"]

    # adding column to app_df
    app_df["applicant_MTSP_Income_Limit"] = merged["value"]

    return app_df
