# Exploratory Data Analysis

## Data Preparation documentation
### Data preparation for Resale datasets
1. Recorded differences in counts between *TOUCHABLE Resale Transaction Info* (Old cleaned dataset) and **Resale Transaction Info updated Sept 2025** (New dataset), to check for new data to be added to the cleaned dataset.
2. Within **TOUCHABLE Resale Transaction Info,** final\_round2 sheet was used, since it appeared to be the latest cleaned version of the Resale Transaction Info dataset by the previous team.  
3. Parsed and concatenated address fields into structured columns (Town, Development, Address, Unit Number) for **Resale Transaction Info updated Sept 2025**. *Ref: CHAPA\_ParseData.ipynb.* 
4. Checked for discrepancies between New and Old dataset, and saved a csv of the new Sept 2025 entries that weren't present in Old dataset. *Ref: DisparityCheckforProperties\_resale\&applicant.ipynb.*  
5. Merged these new entries to the Old cleaned dataset. *Ref: Merging Final Round with updated Sept2025 Resale.ipynb.*  
   

## EDA Documentation by Python Notebook (for Applicant & Resale data)
### 1. Aastha_EDA_resale.ipynb

### 2. Jihyeon_EDA_geocoded_2021_23.ipynb

### 3. Ngo_EDA_Chapter-40B_2023-25.ipynb
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

### 4. Rohan_S2.ipynb

### 5. madison_eda_2021-23.ipynb

## 6. requirements.txt
* `pip install fa25-team-a/eda/requirements.txt` before running the Jupyter Notebook files
