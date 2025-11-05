from __future__ import annotations
import numpy as np
import pandas as pd

def append_resale_data(df: pd.DataFrame):

    """
    This function:
    - takes in the application dataset, 
    - loads in the resale value datasets, 
    - then appends them to the application dataset.
    """

    #app_df = pd.read_parquet("data/processed/applications_clean.parquet")

    # import price data 
    prices_1 = pd.read_excel('data/raw/Resale_Values_Jun_2021_to_Sept_2023.xlsx')
    prices_2 = pd.read_excel('data/raw/Resale_Values_May_2025_to_Sept_2025.xlsx')

    # concatinating the two prices
    prices = pd.concat([prices_1, prices_2])
    price_map = prices.set_index("Application Property").to_dict(orient="dict")['Maximum Resale Price']

    df["Property Maximum Resale Price"] = df["Application Property"].map(price_map)

    return df






