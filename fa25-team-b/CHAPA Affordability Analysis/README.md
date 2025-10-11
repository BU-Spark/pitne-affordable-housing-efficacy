This script analyzes real housing application data from CHAPA’s Chapter 40B Affordable Housing Program (2021–2023).  
The goal is to understand the financial background of applicants — their **income**, **assets**, and **overall wealth patterns** — using Python.

This Script:
- Loads the original Excel data file containing CHAPA applicants.
- Cleans and filters the data to keep only valid, complete applications.
- Calculates new financial metrics like:
  - **Asset-to-Income Ratio** (how many years of income an applicant has saved)
  - **Total Wealth** (income + assets)
- Groups applicants into categories such as:
  - Low Wealth (<1x)
  - Moderate (1–3x)
  - Comfortable (3–6x)
  - High Wealth (>6x)
- Creates charts that show:
  - The distribution of wealth ratios
  - The relationship between income and assets
- Saves all cleaned data and charts into an organized folder.
