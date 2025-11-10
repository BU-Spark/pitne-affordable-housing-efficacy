
# Data Analysis and Visualization
Date: Nov 9, 2025

## Project Base Questions
1. Movement and Distance Analysis
    - a. How far from their current homes, do applicants apply for these affordable homeownership opportunities?
    - b. How does the applicant geographic range compare between different demographic groups? (e.g., race, household type, age, marketing source, etc.). Are local applicant demographics similar or different from more distant applicants?
2. Portfolio Effects: To what extent are the applicant demographics driven by CHAPA’s limited property pool (suburban, age-restricted homes) versus applicant choice?
3. Price: Does the price of the affordable home affect applicant quantity and demographics, controlling for income limits?

---

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

---

### Resale & Prices Data (2021-25)
#### Data Sources

*Datasets provided by **CHAPA** and used in the data pipeline:*

**Resale Data**
- **File:** `Resale Transaction Info - Confidential_updated Sept 2025`

**Price Data**
- **Original Files:**
  - `Resale Values_Jun 2021 to Sept 2023.xlsx`
  - `Resale Values_Oct 2023 to May 2025.xlsx`
  - `Resale Values_May 2025 to Sept 2025.xlsx`

- **Supplementary File (for missing resale properties):**
  - `Property_Data_Jun2021_Sep2025_MissingResaleValues_Completed.csv`
  - **Note:** This file was provided after the original workflow was executed. To include this data in the pipeline, please follow the **New Workflow** section below.

--

#### Original Workflow (Executed)

The **original workflow** was actually run to produce datasets for analysis. Steps included:

##### 1. Parsing and Cleaning
**Resale Data**
- Clean missing values, inconsistent formats, and extraneous text.
- **Output File:** `ParsedResale_updatedSept2025_New.csv`

**Price Data**
- Combine June 2021 – September 2025 price files into a single CSV (`PriceMerge_Jun21_Sept25.csv`) using Excel.  
- Parse concatenated `Application Property` column into:
  - **Town**  
  - **Street Address**  
  - **Unit Number**  
- Extract property features such as `(55+)`, `(first come first serve)`, `(age restricted)` into **Property Feature**  
- **Output File:** `Jun21_Sept25_Parsed.csv`

##### 2. Dataset Integration
**Merge Price and Resale**
- Merge parsed price and resale datasets using keys: `Town`, `Address`, `Unit Number`
- **Output File:** `merged_dataset_price&resale_Sept25.csv`  
- Validate for unmatched, duplicate, or misformatted rows

**Merge Applicants with Properties**
- Load `merged_dataset_price&resale_Sept25.csv` and cleaned applicant data:
  `CHAPA_Chapter-40B_Application-Data_2021-2025_merged_v0.3.csv`
- Standardize columns for merging (`Town_clean`, `Address_clean`, `Unit_clean`)
- Perform **left join** to retain all property records
- **Output File:** `merged_properties_with_applicants.csv`

##### 3. Handling Missing Prices (Supplementary Data)
- Supplementary price file was **not included** in this workflow  
- To fill missing maximum resale prices:
  - Merge `merged_properties_with_applicants.csv` with `Property_Data_Jun2021_Sep2025_MissingResaleValues_Completed.csv`
  - **Output File:** `new_merged_dataset_filled.csv`

##### Notebooks (Original Workflow)
**Location:** `fa25-team-a/analysis/resale_price_original_workflow`

1. `Ria_ParseResaleData.ipynb`  
2. `Ria_ParsePrices_OriginalWorkFlow.ipynb`  
3. `Ria_Merge_Resale&Price_OriginalWorkFlow.ipynb`  
4. `Ria_Merge_PriceResaleApplicantData_OriginalWorkFlow.ipynb`

--

#### Recommended New Workflow (Streamlined for Supplementary Prices)

The **new workflow** integrates supplementary price data **before merging with resale**, providing a cleaner, fully reproducible pipeline.

##### 1. Parsing and Cleaning
- Parse resale and original price data as before
- Merge supplementary price data with the original price dataset **before merging with resale**
- **Output File:** `PriceData_Filled.csv`

##### 2. Merge Price and Resale
- Merge updated price dataset (original + missing prices) with resale dataset
- **Output File:** `MergedPrice_Resale_Full.csv`
- **Notebook:** `Ria_Merge_Resale&Price_NewWorkFlow.ipynb`

##### 3. Merge with Applicant Data
- Merge `MergedPrice_Resale_Full.csv` with cleaned applicant dataset:
  `CHAPA_Chapter-40B_Application-Data_2021-2025_merged_v0.3.csv`
- Fill any missing prices from supplementary dataset if necessary
- **Output File:** `Final_Merged_CHAPA_Dataset.csv`
- **Notebook:** `Ria_Merge_PriceResaleApplicantData_NewWorkFlow.ipynb`

##### Notebooks (New Workflow)
**Location:** `fa25-team-a/analysis/resale_price_new_workflow`

1. `Ria_ParseResaleData.ipynb`  
2. `Ria_ParsePrices_NewWorkFlow.ipynb`  
   > Includes step to merge missing prices before resale merge  
3. `Ria_Merge_Resale&Price_NewWorkFlow.ipynb`  
4. `Ria_Merge_PriceResaleApplicantData_NewWorkFlow.ipynb`

--- 
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

---

## Next Steps
###  Price Analysis
- Explore **interaction effects** between price and demographics (race, household type, age group) to understand nuanced affordability patterns.
- **Finalize Distance Metrics:** Validate geocoding accuracy and confirm the definition of “local” vs “non-local” applicants. Finalize whether to use **county-level aggregation** or a finer geographic unit (town or ZIP) for distance calculations.
- **Clarify Base Question 2 (Portfolio Effects):** Revisit the analysis with complete demographic data now available, incorporating clearer distinctions for:
   - **FTHB (First-Time Home Buyer)** vs non-FTHB applicants  
   - **Age-restricted** vs unrestricted properties  
   - Expanded demographic variables (race, household type, income, age)
   These refinements will enable more accurate interpretation of how CHAPA’s property pool influences applicant diversity and choice.

--- 
## Initial Analysis Results
### 1. Movement and Distance Analysis
* Strong In-State Concentration: About 95 % of applicants are from Massachusetts, with neighboring NH (57 %) and RI (23 %) forming the bulk of the remainder — confirming CHAPA’s programs primarily serve a regional audience.

* Localized Demand Patterns: Most applicants live within 25 km of their chosen property, implying affordability demand is highly local. Larger distances tend to come from younger and non-White applicants.

* Spatial & Demographic Segmentation:

  - Boston–Cambridge MSA attracts younger, racially diverse applicants.

  - Cape Cod & Central MA towns show older, predominantly White applicants linked to age-restricted housing.

* Portfolio-Linked Repeat Behavior: Repeat applications cluster in high-inventory towns such as Andover, Ayer, and Braintree, suggesting movement is guided more by property availability than by relocation interest.

### 2. Portfolio Effects
* Age-Restriction Drives Demographics:

  - 55+/62+ properties have 75–100 % White applicants.

  - Unrestricted properties are substantially more diverse (≈ 40 % non-White).

  - Regression confirms that a higher share of age-restricted units → older median applicant age.

* Racial Segregation by Town:

  - Suburban/exurban towns (Ayer, Northborough, Medway) remain majority White.

  - Urban-adjacent towns (Braintree, Canton, Tyngsborough) show the highest racial mix.

  - Multiracial applicants cluster where new developments are concentrated, e.g. Bedford, Billerica, Milford.

* Marketing Channel Disparities:

  - MyMassHome and Zillow/Trulia dominate outreach (~60 % of total applications) but skew heavily White.

  - City of Boston MetroList and Word of Mouth channels yield higher Black and Hispanic participation.

  - Social Media/Local Community channels remain underutilized yet attract the most diverse proportions.

* Financial & First-Time Buyer Divide:

  - Median assets cluster around $40 k – $60 k, with outliers > $250 k mainly from older applicants.

  - Towns with many 55+ properties (e.g. Andover, Orleans) exhibit near-universal first-time homebuyer rates, showing programs capture downsizing seniors entering ownership rather than long-term renters.

### 3. Price

**Initial Findings:**  
Regression and demographic analyses show that within the affordable range (below 80% AMI), **price does not significantly affect applicant volume or composition**.  
Higher-priced homes attract slightly fewer applicants, but this relationship is statistically weak.  
**Lower-income groups (<$60k)** show more price sensitivity, while higher-income and racial groups display consistent participation across price levels.  
This indicates that **factors like location, property type, and accessibility** play a greater role in driving applicant demand than minor price differences.





--- 
## Notebook Requirements
* requirements.txt
   * `pip install -r fa25-team-a/eda/requirements.txt` before running the Jupyter Notebook files
