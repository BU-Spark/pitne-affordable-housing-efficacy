
# Data Analysis and Visualization
Date: Nov 9, 2025

## Project Base Questions
1. Movement and Distance Analysis
    a. How far from their current homes, do applicants apply for these affordable homeownership opportunities?
    b. How does the applicant geographic range compare between different demographic groups? (e.g., race, household type, age, marketing source, etc.). Are local applicant demographics similar or different from more distant applicants?
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
    * `./Chapter-40B_zip_long_lat.ipynb`
* Visualizing:
    * `./Ngo_q1_viz.ipynb`
    * `./Ngo_q2_viz.ipynb`

### Resale & Prices Data
#### Pipeline:
* 
#### Notebooks:
* 


## Next Steps


## Initial Analysis Results
### 1. Movement and Distance Analysis
* 
* 

### 2. Portfolio Effects
* 
* 

### 3. Price
* 
* 


## Notebook Requirements
* requirements.txt
   * `pip install -r fa25-team-a/eda/requirements.txt` before running the Jupyter Notebook files
