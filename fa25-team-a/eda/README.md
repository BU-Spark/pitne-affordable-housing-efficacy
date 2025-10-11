# Exploratory Data Analysis

## Data cleaning, preparation, and preliminary visualization
### Resale Transaction datasets
* Pipeline:
   1. Recorded differences in counts between *TOUCHABLE Resale Transaction Info* (Old cleaned dataset) and **Resale Transaction Info updated Sept 2025** (New dataset), to check for new data to be added to the cleaned dataset.
   2. Within **TOUCHABLE Resale Transaction Info,** final\_round2 sheet was used, since it appeared to be the latest cleaned version of the Resale Transaction Info dataset by the previous team.  
   3. Parsed and concatenated address fields into structured columns (Town, Development, Address, Unit Number) for **Resale Transaction Info updated Sept 2025**. *Ref: CHAPA\_ParseData.ipynb.* 
   4. Checked for discrepancies between the New and Old datasets, and saved a CSV file of the new Sept 2025 entries that weren't present in the Old dataset. *Ref: DisparityCheckforProperties\_resale\&applicant.ipynb.*  
   5. Merged these new entries into the Old cleaned dataset. *Ref: Merging Final Round with updated Sept2025 Resale.ipynb.*  
* Notebooks:
   * Aastha_EDA_resale.ipynb

### Chapter 40B Applicant datasets
#### 2021-23
* Dataset: TOUCHABLE CHAPA Chapter 40B Application Data 2021-2023 & 10|2023-05|2025
(https://docs.google.com/spreadsheets/d/1xcW0qveqOPD-1JvJX1jaSJjPyCVVMGbY/edit?gid=690813037#gid=690813037)
* Sheet used: Geocoded Kayla 2021-2023, CLEAN w stats Kayla 2021-2023
* Pipeline:
   1. Explore the sheets and select one which covers up all the other sheets and one with geocoded data
   2. Extract zip values from 'Matched Address' and fill 'ZIP' null values
   3. Analyze the movement and distance trends across different demographic groups
   4. Preprocess the dataset: replace age median to round value, deal with null values, visualizing
   5. Check blockers for blockers: difference between 'Race/Ethnicity' and 'Census Race' categories (e.g. Hispanic/Latino) require clarification, further gecoded data needed
* Notebooks:
   * Jihyeon_EDA_geocoded_2021_23.ipynb
   * madison_eda_2021-23.ipynb

#### 2023-25
* Dataset: TOUCHABLE CHAPA Chapter 40B Application Data 2021-2023 & 10|2023-05|2025 (https://docs.google.com/spreadsheets/d/1xcW0qveqOPD-1JvJX1jaSJjPyCVVMGbY/edit?gid=690813037#gid=690813037)
* Sheet used: 23-25_data_updated
* Pipeline:
   1. Load Excel file
   2. Explore sheets and pick the most completed and updated sheet as the dataset to be cleaned
   3. Explore dataset: data types, null values, all columns
        * Note all findings in a Markdown table
   4. Outline next steps to manipulate the dataset: questions to ask clients, cleaning methods, and creating new columns
        * Will perform more EDA using clarification from the Oct 10 client meeting
* Notebooks:
   * Ngo_EDA_Chapter-40B_2023-25.ipynb
      * `zip` null values can be extracted from `matched_address`
      * further geocode to fill the rest of `matched_address `
      * need help from client in handling null values and outliers in some columns (e.g., `age`, `hh_income`)
   * Rohan_S2.ipynb

## Requirements
* requirements.txt
   * `pip install fa25-team-a/eda/requirements.txt` before running the Jupyter Notebook files
