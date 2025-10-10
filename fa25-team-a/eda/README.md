# Exploratory Data Analysis

## 1. Aastha_EDA_resale.ipynb

## 2. Jihyeon_EDA_geocoded_2021_23.ipynb

## 3. Ngo_EDA_Chapter-40B_2023-25.ipynb
* Dataset: TOUCHABLE CHAPA Chapter 40B Application Data 2021-2023 & 10|2023-05|2025 (https://docs.google.com/spreadsheets/d/1xcW0qveqOPD-1JvJX1jaSJjPyCVVMGbY/edit?gid=690813037#gid=690813037)
* Sheet used: 23-25_data_updated
* Pipeline:
    * Load Excel file
    * Explore sheets and pick the most completed and updated sheet as the dataset to be cleaned
    * Explore dataset: data types, null values, all columns
        * Note all findings in a Markdown table
    * Outline next steps to manipulate dataset: questions to ask clients, cleaning methods, creating new columns
        * Will perform more EDA using clarification from Oct 10 client meeting
* Summary:
    * `zip` null values can be extracted from `matched_address`
    * further geocode to fill rest of `matched_address `
    * need help from client in handling null values and outliers in some columns (e.g., `age`, `hh_income`)

## 4. Rohan_S2.ipynb

## 5. madison_eda_2021-23.ipynb

## 6. requirements.txt
* `pip install fa25-team-a/eda/requirements.txt` before running the Jupyter Notebook files