
# Data Analysis and Visualization
Date: Nov 9, 2025

## Project Base Questions
1. Movement and Distance Analysis
    - a. How far from their current homes, do applicants apply for these affordable homeownership opportunities?
    - b. How does the applicant geographic range compare between different demographic groups? (e.g., race, household type, age, marketing source, etc.). Are local applicant demographics similar or different from more distant applicants?
2. Portfolio Effects: To what extent are the applicant demographics driven by CHAPA’s limited property pool (suburban, age-restricted homes) versus applicant choice?
3. Price: Does the price of the affordable home affect applicant quantity and demographics, controlling for income limits?


## Work Completed
### Applicant Data (2021-25)
#### Pipeline:
* Merge, clean, and standardize 2021-23 and 2023-25 CHAPA Chapter 40B Applicant datasets
* Geocode
    * `current_residence_zip` from `current_residence_town_city` and `current_residence_state`
    *  Longitudes and latitudes for Current Residence and Property Addresses
* Calculate distance between longitude and latitude combinations of Current Residence and Property Addresses
* Create `current_county` and `property_county` using a Massachussetts county and city list
* Categorize applications into local (if current residence town and property town are in the same county) vs. distant
* Merge with Resale and Prices dataset on Property Address, Unit, and Town
* Analyze and visualize for Base Questions 1 and 2
#### Notebooks:
* Merging and cleaning:
    * US cities dataset to clean: `../data/us-cities.txt`
    * `../eda/Ngo_Chapter-40B_merged.ipynb`
    * `../eda/Rohan_EDA_RaceCleaning_2021_25.ipynb`
* Populating geographical info columns:
    * MA county and city dataset: https://www.mass.gov/doc/metrolstpdf/download
    * `./Jihyeon_Chapter-40B_zip_long_lat.ipynb`
* Visualizing:
    * `./Ngo_q1_viz.ipynb`
    * `./Ngo_q2_viz.ipynb`
    * `./madison_eda_2021-23.ipynb`
    * `./madison_eda_2_2021-23.ipynb`
    * `./madison_merged_data_analysis.ipynb`

### Resale & Prices Data (2021-25)
#### Data Sources

*Datasets provided by **CHAPA** and used in the data pipeline:*

#### Resale Data
- **File:** `Resale Transaction Info - Confidential_updated Sept 2025`

#### Price Data
- **Original Files:**
  - `Resale Values_Jun 2021 to Sept 2023.xlsx`
  - `Resale Values_Oct 2023 to May 2025.xlsx`
  - `Resale Values_May 2025 to Sept 2025.xlsx`

- **Supplementary File (for missing resale properties):**
  - `Property_Data_Jun2021_Sep2025_MissingResaleValues_Completed.csv`
  - **Note that this file wasn't used in the pipeline since it was provided after this pipeline was done running.** To replicate this pipeline please run **(NOTEBOOK NAME)** to include data from the Supplmentary file.

#### Pipeline:
1. **Initial Cleaning**  
   - Clean the **resale** and **price** datasets separately to handle missing values, inconsistent formats, and extraneous text.  

2. **Data Parsing & Feature Extraction**  
   - Using Excel, combine all June 2021–September 2025 price data into a single file.  
   - Parse the concatenated **Address** column into standardized components for easier merging and analysis:  
     - **Town**  
     - **Street Address**  
     - **Unit Number**  
   - From the price dataset, extract comments such as *(age restricted)*, *(first come first serve)*, and *(55+)* into a new column called **Property Feature**.  
   - **Output Files:**  
     - `ParsedResale_updatedSept2025_New.csv` — parsed resale data  
     - `Jun21_Sept25_Parsed.csv` — parsed price data  

3. **Dataset Integration**  
   - Merge both output datasets using the combined keys **(Town, Address, Unit Number)** as the primary identifiers.  
   - Save the merged dataset as `merged_dataset_price&resale_Sept25.csv`.  
   - Validate the join by checking for unmatched, duplicate, or incorrectly formatted entries.  

#### Notebooks:
* 

### Merged master files for answering differnt base questions
#### Dataset in reference:

#### Property (Price & Resale) Data (that we get from previously mentioned Resale & Prices Data pipeline)
- **File:** `merged_dataset_price&resale_Sept25.csv`

#### Applicant Data (that we get from Applicant Data pipeline)
- **File:** `CHAPA_Chapter-40B_Application-Data_2021-2025_merged_v0.3.csv`

#### Supplementary Price Data
- **File:** `Property_Data_Jun2021_Sep2025_MissingResaleValues_Completed.csv`


#### Pipeline

1. **Load Datasets**  
   - Import the **Property (Price & Resale)**, **Applicant**, and **Supplementary Price** datasets into pandas.  
   - These collectively include property-level resale information, Chapter 40B applicant data, and additional price data for missing records.

2. **Column Standardization for Merging**  
   - Create a helper function to clean and standardize key text columns by:  
     - Stripping leading/trailing spaces  
     - Converting all text to lowercase for consistent merging  
   - Align merge keys across datasets:  
     - From **Property Dataset:** `Town`, `Address`, `Unit Number`  
     - From **Applicant Dataset:** `property_town_city`, `property_street_address`, `property_unit`  
   - Generate standardized columns: `Town_clean`, `Address_clean`, and `Unit_clean`.

3. **Merge Applicants with Properties**  
   - Perform a **left join** between the Property and Applicant datasets using the standardized columns.  
   - This ensures that **all property records are retained**, even if corresponding applicants are missing.  
   - This join structure is crucial for **analyzing how property characteristics and resale prices influence applicant patterns** — directly addressing the **third base question** in the analysis.  
   - Drop helper columns (`Town_clean`, `Address_clean`, `Unit_clean`) after merging.  
   - **Output File:**  
     - `merged_properties_with_applicants.csv`

4. **Fill Missing Maximum Resale Prices**  
   - Load the merged dataset and the **Supplementary Price Data** containing missing resale prices.
   - Run *Price_Resale_Applicant_MergeV2.ipynb* to merge all three datasets.
   - The final dataset `new_merged_dataset_filled.csv` integrates Property and resale information (with filled maximum resale prices from supplementary records) , Applicant data for Chapter 40B properties  

#### Notebooks
- *Price_Resale_Applicant_MergeV2.ipynb:*
   - Rename the price column for consistency: `Price → Maximum Resale Price`.  
   - Merge supplementary prices using keys **(Town, Address, Unit Number)**.  
   - Fill any missing prices in the main dataset using the newly merged data.  
   - Drop helper columns after imputation.  
   - **Final Output File:**  
     - `new_merged_dataset_filled.csv`
    
### Price Analysis and Demographic Insights

**Objective:**  
Evaluate whether the resale price of affordable homes affects applicant quantity and demographic composition, while controlling for income limits.

**Methods & Work Completed:**  
- **Data Cleaning:** Standardized `Maximum Resale Price` and `hh_income` fields, removed symbols, and converted text-based income ranges into numeric values.  
- **Data Aggregation:** Grouped applicants by `Matched Address` to calculate average resale price, average applicant income, and total applicant count per property.  
- **Modeling:** Ran Ordinary Least Squares (OLS) regression models to test whether price predicts applicant count while holding income constant.  
- **Visualizations:**  
  - *Applicant Count vs. Price (OLS Trend)* –shows slight negative slope but statistically insignificant relationship.  
  - *Correlation Heatmap (Price,Income, Applicant Count)* – weak correlation, confirming minimal price impact.  
  - *Correlation by Income Bracket* – highlights that lower-income applicants (<$60k) are more price-sensitive than higher-income brackets.  
  - *Average Price by Race* – explores whether price distribution differs across racial groups, showing no major disparities.  
- **Demographic Extension:** Expanded analysis to assess race and income diversity across property price levels.

**Notebooks Reference:**  
- `Aastha__full_merged_V1_analysis.ipynb`- performs price sensitivity modeling and regression analysis.  
- `Aastha_Demographic and applicant vs price analysis.ipynb`- explores racial and demographic patterns in price sensitivity.  



## Next Steps
###  Price Analysis
- Explore **interaction effects** between price and demographics (race, household type, age group) to understand nuanced affordability patterns.


## Initial Analysis Results
### 1. Movement and Distance Analysis
* 
* 

### 2. Portfolio Effects
* 
* 

### 3. Price

**Initial Findings:**  
Regression and demographic analyses show that within the affordable range (below 80% AMI), **price does not significantly affect applicant volume or composition**.  
Higher-priced homes attract slightly fewer applicants, but this relationship is statistically weak.  
**Lower-income groups (<$60k)** show more price sensitivity, while higher-income and racial groups display consistent participation across price levels.  
This indicates that **factors like location, property type, and accessibility** play a greater role in driving applicant demand than minor price differences.






## Notebook Requirements
* requirements.txt
   * `pip install -r fa25-team-a/eda/requirements.txt` before running the Jupyter Notebook files
