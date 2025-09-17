***Project Information*** 

* What is the project name?


Team CHAPA: Improving Access to Affordable Homeownership
* What is the link to your project’s GitHub repository?
[Link](https://github.com/BU-Spark/pitne-affordable-housing-efficacy.git)  
* What is the link to your project’s Google Drive folder? \*\**This should be a Spark\! Owned Google Drive folder \- please contact your PM if you do not have access\*\**
[Link](https://drive.google.com/drive/folders/1OhYmg-8f7ar-rGoFBal5h7by8BbwKDbe?usp=drive_link)
* In your own words, what is this project about? What is the goal of this project?

Our project's goal is to assist CHAPA in its mission to expand homeownership to households from disadvantaged, lower-income, or underrepresented backgrounds by analyzing patterns and trends in their Chapter 40B housing application data collected to understand who is applying where, and what disparities are faced by different demographics. With this, we are also answering questions about where individuals discover CHAPA's 40B housing. Our analysis is intended to support their marketing and outreach strategies such that they can reach their target audience and better connect with underserved populations who can benefit from affordable housing and their services. 
* Who is the client for the project?

CHAPA: Citizens’ Housing and Planning Association  
* Who are the client contacts for the project?

David Gasser  
* What class was this project part of?

PIT-NE Impact Tech Fellowship Summer 2025

***Dataset Information***

* What data sets did you use in your project? Please provide a link to the data sets, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.

We used 3 datasets. Two were application datasets with data from 2021-2023 and 2023-2025, respectively. The other data was on Resale Transaction information. These datasets are confidential and can only be accessed with authorization.

* What keywords or tags would you attach to the dataset?  
  * Domain(s) of Application: Civic Tech, Housing, Affordable Homeownership, Policymaking, Community Development


*The following questions pertain to the datasets you used in your project.*   
*Motivation* 

* For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description. 

The datasets were created for data analysis and making visualizations for this specific project.  

*Composition*

* What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? What is the format of the instances (e.g., image data, text data, tabular data, audio data, video data, time series, graph data, geospatial data, multimodal (please specify), etc.)? Please provide a description.

All 3 datasets were shared in the form of spreadsheets. 
Application Datasets: Each instance in these datasets represents an application to an affordable housing unit managed by CHAPA.
Resale Transaction dataset: Each instance in this dataset provides information on the transaction for the winner of the lottery for a particular resale unit. 
I worked heavily with the second application dataset with applications from 2023 to 2025. 

* How many instances are there in total (of each type, if appropriate)?

In the application dataset for 2023-2025, there were 1360 instances or rows before cleaning.

  
* What data does each instance consist of? “Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description.

It is a mix of standardized text fields, numerical values and free text responses.

* Is there any information missing from individual instances? If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include redacted text.

 There are intentionally no personal identifiers in our dataset to protect the identity of applicants.
   
* Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset? If so, please describe how.

No, it is not possible.


| Size of dataset |  |
| :---- | :---- |
| Number of instances |1360|
| Number of fields  |18|

  
*Collection Process*

* What mechanisms or procedures were used to collect the data (e.g., API, artificially generated, crowdsourced \- paid, crowdsourced \- volunteer, scraped or crawled, survey, forms, or polls, taken from other existing datasets, provided by the client, etc)? How were these mechanisms or procedures validated?

 The application dataset for 2023-2025 was collected through CHAPA's online application submission form. 
 
* Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent crawl of old news articles)? If not, please describe the timeframe in which the data associated with the instances was created.

2023 to 2025 

*Preprocessing/cleaning/labeling* 

* Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? If so, please provide a description. If not, you may skip the remaining questions in this section.

# Round 1 Data Cleaning and Processing
1. **Create a Copy**
   - Created a copy of the sheet within the same spreadsheet document.

2. **Initial Observations**
   - Observed general properties of the data and took notes.

3. **Removing Irrelevant Data**
   - As informed by David, bolded values are not relevant.
   - Unbolded those rows in my copy of the sheet.

4. **Sorting the Data**
   - Sorted the sheet by **Closing Date** to better organize rows with and without values.

5. **Download and Setup**
   - Downloaded a `.csv` file of the copy of the Google Sheet.
   - Set up Jupyter, Python, Pandas, and VSCode on local computer.

6. **Data Parsing**
   - Split the **"Town - Development - Address"** column into 4 new columns:
     - **Town**
     - **Development**
     - **Address**
     - **Unit Number**
   - Original structure of the column:  
     `"Town - Development</br>Address</br>Unit: Unit Number"`

7. **Script Management**
   - Added the data cleaning script to the GitHub folder.

8. **Import Cleaned Data**
   - Imported the cleaned version from local machine into the spreadsheet as **Round1**.

9. **Manual Cleanup**
    - Manually highlighted confusion points in the **Round1** sheet.
    - Deleted the original **"Town - Development - Address"** column in **Round1**.

10. **Duplicate Sale Detection**
    - Wrote a script to identify units that were resold.
    - Manually confirmed the duplicates detected by the script.

12. **Additional Enhancements**
    - Added a column for the corresponding **MSA**.
      - *Reasoning:* MSAs are referenced in background readings for minority balancing and might be helpful for analysis.
    - Refer to Round 2 for steps around geocoding

14. **Final Cleanup**
    - Deleted local files after confirmation.

# Round 2 Data Cleaning and Geocoding

## Data Cleaning for Resale Transactions Dataset

### 1. Missing Bedroom Information
- Searched online for the number of bedrooms for 4 properties maintained by **CHAPA** that were missing this data.

### 2. Sorting and Download
- Sorted the sheet by **Transaction Start Date**.
- Downloaded the spreadsheet for **Round 2**.

### 3. Date Column Conversion
- Changed **Start Date** and **Closing Date** columns from string objects to datetime format for efficient processing.

### 4. Transaction Filtering Script
- Wrote a script that:
  - Identifies rows where:
    - `Transaction Start Date` < **2024-09-01**
    - `Closing Date` is empty or null.
  - Counts the number of such rows.
  - Temporarily sets their `Closing Date` to **1900-09-01**.
    - *Purpose:* Flagged for David to clarify if data is missing or if sales were never completed.
  - Leaves other null `Closing Date` values as blank.
- Added the script to my branch on **GitHub**.
- Updated these dates later into the project after receiving info from CHAPA

### 5. Age Restricted Column Standardization
- Sorted the sheet by the **Age Restricted** column.
- Manually changed:
  - `'Some 55+'` → `'55+'`
- Wrote a script to:
  - Fill missing/null values in the **Age Restricted** column with `'No'`.
  - Later reverted those `'No'` values back to `null` based on client feedback.
- Imported the updated `.csv` into the spreadsheet as a **duplicate**.
- Copied the cleaned column into the **Round 2** sheet.
- Deleted the temporary duplicate sheet.
- Added this script to my branch on **GitHub**.

### 6. Geocoding Process

#### Preparation
- Sorted sheet by **Town** for easier review.
- Created a plan:
  - Prepare imports and DataFrame.
  - Add a **Unique ID** column to the CSV as required by the census geocoder API.
  - Use **batch geocoding** to obtain standardized addresses.

#### MSA Matching
- Accessed corresponding MSAs **row by row**.
- Created a new DataFrame with the following new columns:
  - `Match Status`
  - `Match Type`
  - `Matched Address`

#### Manual Review
- Manually reviewed **21 street addresses** that the Census API could not match or associate with an MSA. Maybe because MSA data changes every so often.

* Were any transformations applied to the data (e.g., cleaning mismatched values, cleaning missing values, converting data types, data aggregation, dimensionality reduction, joining input sources, redaction or anonymization, etc.)? If so, please provide a description.

Answered in detail below

 ## Data Cleaning for Applications Dataset 2023-2025
The raw dataset consisted of 1360 rows and 14 columns.
Some of the data cleaning was done in google spreadsheets. This involved splitting of property street addresses into street address, unit, town and state. 
### Variables
1. Submission Date: This field was not in first normal form and so the date was split into submission date, time and year.
2. Application property: This was also split into property town, street address, unit and state.
3. Source: 44 unique values, 3 missing values.
   
   Source was standardized into the following categories based on the CHAPA submission form:

   <img width="219" alt="Screenshot 2025-06-29 at 7 18 23 PM" src="https://github.com/user-attachments/assets/39c95e88-e9e9-4c6d-bbab-4c75a77983d5" />
   
Zillow/Trulia/Etc. was merged with Zillow/Truly/OtherWebsite 
All rows with MyMassHome, Friend/Word of Mouth, City of Boston Metrolist, Real Estate Agent and Social Media  were copied as is. Any names of real estate agents were counted under 'Real Estate Agents'. Redfin (6 entry) considered under “other websites”. Any entries with mass.gov were considered as MyMassHome. Similarly, Urban Edge Housing (2 entries) considered as other website, 
Merrimack Valley Housing Partnership (2 entries) considered as other website and 
Martha's Vineyard Dukes County Regional Housing Authority ( 3 entries) considered as other.  

4. Race Ethnicity: 62 unique values, 3 missing values.

Race and ethnicity were first standardized into CHAPA submission form     categories, recording multiple race entries using ";" as separator. These were later normalized into CHAPA submission form categories plus a "Multiple Races/Ethnicites" category for people who chose more than one. Race was further simplified into "Race Simplified" which categorised any person who selected "Hispanic or Latino" (even if they chose multiple races) to "Hispanic or Latino (of any race)". Lastly, race was standardized to census race categories, for example, "Middle Eastern or North African" was simplified to "White" as per census guidelines. 

5. Age: 1 missing value, Max value: 86, Min: 0. While making visualizations, applicants with age under 10 and missing values were eliminated.
6. Current Residence: Current residence was split into town and state
7. Household Type: 41 unique values. Houshold type was normalized into CHAPA submission form categories. 
8. Household Income: 5 missing values (eliminated in visualizations). We made corrections to certain values that were confirmed to be errors. A new variable called "Income Brackets" was created to simplify visualizations.
9. Household Assets: 1 missing value (eliminated during visualizations). A new variable called "Asset Brackets" was created to simplify visualizations.
10. FTHB: 3 missing values (eliminated during visualizations)

### Geocoding
#### MSA
Used Ari's prepared code to match MSA values based on street addresses of properties using the census API. This also helped create the "matched_address" column that matched and standardized property street addresses to street addresses recorded in the census data.

#### Latitude & Longitude 
Used Kayla's prepared code to match latitude and longitude for properties based on street addresses using the census API.  

### Area Median Income 
Used the HUD API to identify Area Median Income for each application. Based on the property MSA, the API was used to find the AMI of MSA as well as different income brackets that categorised individials as low, extremely low or very low. Each applicant's income was compared to their MSA's specific income brackets and they were categorised into "low", "extremely low", "very low" or "above low" categories. 

### Merging Datasets
In the file called merging.ipynb, 2 new columns were added to both the 2021-2023 and 2023-2025 application datasets, these were called "bedrooms" and "age_restricted". Using the matched_address columns that were common across datasets through geocoding, properties in application datasets were matched with ones in resale transaction dataset, and information regarding number of bedrooms and whether a property is age-restricted or not, which is only available in resale transaction data, were added to the new "bedrooms" and "age-restricted" columns in the application datasets. 

### Demographic Datasets 
In the Round_1_2025 cleaning script, separate dataset for demographic analysis was created. Duplicated in the "ID number" column were identified and a new dataset containing only the first entry from every unique "ID number" was kept. This subset is representative of the demographic information of applicants avoiding double counting and repeats. This was used to make visualizations answering any demographics related questions. 

### ArcGIS
The arcgis.ipynb script in data_cleaning folder was used to create datasets with percentage calculations as needed for visualizations in ArcGIS. 



* Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? If so, please provide a link or other access point to the “raw” data, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.

Yes, the raw data was unmodified in the original dataset spreadsheets, we created copies of the files to do data cleaning. The datasets are confidential and so links cannot be shared. 

* Is the code that was used to preprocess/clean the data available? If so, please provide a link to it (e.g., EDA notebook/EDA script in the GitHub repository). 

Yes, the code that was used to preprocess and clean the data is available in the scripts provided in data_cleaning folder. [Link](https://github.com/BU-Spark/pitne-affordable-housing-efficacy/blob/Saniya/data_cleaning/Round_1_2025.ipynb )

*Uses* 

* What tasks has the dataset been used for so far? Please provide a description.

Data Analysis and creating Visualizations.

* What (other) tasks could the dataset be used for?

Data analysis -> Visualizations for our report and for our presentations

* Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?

Data is confidential.

* Are there tasks for which the dataset should not be used? If so, please provide a description.

n/a


*Distribution*

* Based on discussions with the client, what access type should this dataset be given (eg., Internal (Restricted), External Open Access, Other)?
Internal access only. Only authorised people from Spark and CHAPA team can and should access the data. 


*Maintenance* 

* If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? If so, please provide a description. 

N/A - Datasets are confidential to our client.

*Other*

* Is there any other additional information that you would like to provide that has not already been covered in other sections?

Yes, I have included several scripts in the folders and want to clarify the location and use for each script:

In summary_statistics_and_visualizations:

new_sum_stat: Visualizations for full datasets and some combined datasets visualizations 

new_dem_sum_stat: Visualizations for demographic datasets that provide information on 'applicants' rather than application. 

In the data_cleaning folder: 

Round_1_2025: Detailed cleaning of variables including standardization of a lot of free text. Creation of demographic datasets.

ami.ipynb: Using HUD API to collect area median income data and categorising applicants into low, very low, extremely low and above low income categories

arcgis.ipynb: Datasets for ArcGIS visualizations and summary statistics for the combined merged dataset.

geocoding.ipynb: Using census API to extract MSA and matched addresses. 

merging.ipynb: This script was used to extract information on bedrooms and age restricted properties by matching addresses across the application datasets and resale transactions datasets. 

The visualizations that we made for the report involved scripts written in python. Those scripts are in the dataset-documentation directories for each of the datasets on the main branch. Similarly, the data cleaning scripts are also in the dataset-documentation directory.


## Data Cleaning for Applications Dataset 2021-2023

### Round 1 Data Cleaning

The application dataset underwent comprehensive cleaning to ensure consistency, resolve ambiguities, and prepare the data for analysis. Cleaning actions included standardization of values, manual geographic validation, correction of typographical errors, handling of missing values, and removal of inconsistencies across categorical entries.

The following summarizes the data cleaning process column by column.

---

#### General Cleaning Steps

- **Whitespace:** Stripped leading and trailing whitespace from all text fields.
- **Capitalization:** Standardized text fields to consistent casing (e.g. title case).
- **Duplicates:** Checked for and found no duplicate rows across the dataset.
- **Special Characters:** Removed question marks and quotation marks from the `Source` column. No additional special character cleaning was needed elsewhere.
- **Missing Value Summaries:** Saved summary reports from all scripts that checked for missing values.

---

#### ID Number

- Field was already standardized upon receipt.
- Checked for missing values (0 found).
- Verified number of unique values (334).
- Created a subset of records for applicants who applied to multiple properties (35 applicants).

---

#### Submission Date

- Field was already standardized upon receipt.
- Checked for missing values (0 found).

---

#### Application Property Address

- Manually verified each address using Google Maps to confirm existence.
- Checked for missing addresses (0 found).
- Counted how many addresses were missing town information (367 found).

---

#### Source

- Created a separate `Source 2` column for any applicants who listed multiple sources. Removed the second source from the primary `Source` field.
- Consolidated similar or variant source names into unified categories:
    - “CHAPA’s list”, “CHAPA”, “CHAPA website” → **CHAPA**
    - “CHAPA email” and “CHAPA Email List” → **CHAPA Email**
    - “friends”, “Family Member”, “family” → **friends and family**
    - “website”, “online”, “internet”, “online research” → **internet (unspecified)**
    - “mass housing website”, “MassHousing” → **MassHousing**
    - “my mass home”, “MyMassHome”, “mymasshome” → **MyMassHome**
    - “boston affordable housing”, “boston.gov” → **boston.gov**
- Deleted all question marks and quotation marks from entries.
- Fixed typographical errors.
- Resolved duplicate multi-source entries:
    - Two applicants entered the same two sources twice. One source was assigned to one of their records, the other source to the second.
- For the entry “family/Mass Ho,” simplified it to “family,” as “Mass Ho” could not be verified as a valid source.

---

#### Age

- Field was already standardized upon receipt.
- Checked for missing values.
- **Missing Values:** Left missing values unfilled due to the high number of missing entries.

---

#### Race/Ethnicity

- Standardized similar terms:
    - “black/afr am”, “black”, “cape vrd blck”, “african amer” → **Black**
    - “White, Black”, “Black/White” → **Mixed race**
    - “Hispanic”, “latino”, “hispanic/latino” → **Latino**
    - “white-north african” → **White**
    - “South Asian Pakistai” → **Asian**
    - “did not list”, “NL” → **Unknown**

---

#### Disability

- Counted how many entries were missing.
- Standardized “Disabled” and “Yes” to a single value: **Yes**.
- **Missing Values:** Filled missing values with “No,” following guidance from CHAPA.

---

#### Current Residence

- Manually reviewed all entries, verifying towns and states using Google Maps.
- Split single field into two fields: **Town** and **State**.
- Entered “MA” as the state if:
    - Town existed in Massachusetts but no state was listed.
- If the town existed in another state:
    - Entered that state into the **State** field.
    - Removed the state from the **Town** field if it was initially embedded there.
    - Highlighted these entries in green to indicate the state was confirmed by the original entry.
- If the town name did not match any Massachusetts locality:
    - Highlighted in red.
    - Added a comment describing the issue.
    - Left **State** field blank.
- For towns that were actually neighborhoods within Massachusetts:
    - Entered “MA” in the **State** field.
    - Highlighted in yellow.
    - Added comments indicating neighborhood adjustment.

---

#### Household Size

- Field was already standardized upon receipt.
- Checked for missing values (0 found).

---

#### Dependents

- Field was already standardized upon receipt.
- Checked for missing values (118 found).
- **Missing Values:** Left missing values unfilled due to the high number of missing entries.

---

#### Household Type

- Field was completely empty in the dataset. No cleaning performed.

---

#### Household Income

- Converted values from currency format to numeric format.
- Checked for missing values (2 found).
- **Missing Values:** Filled missing values with the median income of the dataset.

---

#### Household Assets

- Converted values from currency format to numeric format.
- Checked for missing values (24 found).
- **Missing Values:** Left missing values unfilled due to the high number of missing entries.

---

#### FTHB Class?

- Field was completely empty in the dataset. No cleaning performed.

---

#### Encoding

- No explicit text encoding enforcement was applied; files retained original encoding.



### Geocoding

---

#### MSA
Used Ari's prepared code to match property addresses to addresses recorded in the Census API. This also matched property addresses to a Metropolitan Statistical Area (MSA)

#### Longitude and Latitude
To geocode property addresses, I used the U.S. Census Geocoding Services API. I first created a separate dataframe containing one unique record per address from the `matched_address` field to avoid redundant API calls. For each unique address, I sent a request to the Census geocoding endpoint, which returned latitude and longitude coordinates when a match was found. I implemented a one-second delay between requests to comply with the API’s usage limits. The resulting coordinates were stored in new `latitude` and `longitude` columns in the unique addresses dataframe. Finally, I merged these coordinates back into the original application dataset based on the `matched_address` field and saved the geocoded dataset to a CSV file.

#### Current Residence
Given that only town names and states were provided for current residences, it was not possible to geocode with the Census API. I instead used ArcGIS. I uploaded the file of merged demographic data, selected 'curr_res_full' (town, State) as the location field. I then confirmed all of the matches found by ArcGIS.

### Area Median Income
---
Saniya's code was used to identify the HUD AMI for all application datasets


### Merging Datasets

---

#### Application Datasets Only
In data-cleaning/final_standardization.ipynb I prepared the two application datasets for merging. I dropped columns that were either redundant or not needed for the combined dataset. I then applied consistent renaming across both datasets to ensure columns followed a unified naming convention, using specific mapping dictionaries for each file. After renaming, I checked and confirmed that both datasets shared identical column names. Once standardization was complete, I saved the cleaned files and then concatenated the two datasets to produce a unified application dataset ready for analysis.

#### Merging Applications with Resale Transaction Info
Saniya's code was used to merge the application datasets with the resale transaction info, adding columns for the number of bedrooms and property age restriction to the applications.

### Demographic Datasets
---
The data-cleaning/applicant_df.ipynb script was used to create a dataset containing only 1 entry per applicant. After convsersation with CHAPA, we chose to keep the demographic info from each applicant's first application to best represent each person when they first found a CHAPA property. This was chosen to gear demographic analysis to better answer the question of whether CHAPA's marketing is reaching applicants of different demographics.


### ArcGIS
---
I used data-cleaning/arcGIS_viz_prep.ipynb to prepare the application datasets for analysis and visualization in ArcGIS, I began by reading in the merged application and demographic data files. I created a new indicator to flag whether each application was from a household of color or a white household by mapping race/ethnicities to binary values. I calculated the total number of applications per town and exported this summary for mapping application density across municipalities. To generate a dataset containing only entries with complete property addresses and race/ethnicity entries, I filtered the data to include only records with non-missing, race/ethnicities and valid geographic coordinates and saved this filtered subset. For creating a bivariate choropleth map comparing applications from households of color and white households by town, I grouped the data by town and race indicator, counted the applications, and calculated percentages of applications from households of color and white households within each town before exporting the results. Additionally, I computed each town’s share of the total applications from white households and the total applications from households of color across the entire dataset to visualize how individual towns contribute to the broader regional racial distribution of applications. I also cleaned and standardized all column names for clarity and compatibility with ArcGIS. Lastly, for mapping applicants’ current residences, I combined town and state fields into a single formatted field and saved this demographic dataset for spatial visualization.

### Additional Questions
---

* Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? If so, please provide a link or other access point to the “raw” data, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.

Yes, the raw data was unmodified in the original dataset spreadsheets, we created copies of the files to do data cleaning. The datasets are confidential and so links cannot be shared. 

* Is the code that was used to preprocess/clean the data available? If so, please provide a link to it (e.g., EDA notebook/EDA script in the GitHub repository). 

Yes, the code that was used to preprocess and clean the data is available in the scripts provided in data_cleaning folder. [Link](https://github.com/BU-Spark/pitne-affordable-housing-efficacy/tree/main/data_cleaning)

*Uses* 

* What tasks has the dataset been used for so far? Please provide a description.

Data Analysis, creating vsualizations, writing a report and developing presentations for PIT-NE.

* What (other) tasks could the dataset be used for?

Further analysis and visualizations approved by CHAPA

* Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?

The application datasets only include applications from those that completed their applications. It does not include those that may have started their applications, but did not have the time or resources to complete it. The 2021-2023 dataset was entered manually by hand from paper applications, so the original dataset had many inconcsistencies, and may contain errors. The 2023-2025 dataset was completed as an online portion of the application, contributing to the inconsistenices across the two datasets. Due to manual entry, many entries had to be standardized in the 2021-2023 dataset, particularly in the source column, potentially distorting analysis. 

* Are there tasks for which the dataset should not be used? If so, please provide a description.

The dataset should not be used for identifying personal information of individual applicants. It should also not be used to draw conclusions about the entire affordable housing population given that it only represents the small subset of people who completed applications for CHAPA's 40B resale properties from 2021-2025.


*Distribution*

* Based on discussions with the client, what access type should this dataset be given (eg., Internal (Restricted), External Open Access, Other)?
Internal access only. Only authorised people from Spark and CHAPA team can and should access the data. 


*Maintenance* 

* If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? If so, please provide a description. 

N/A - Datasets are confidential to our client.

*Other*

* Is there any other additional information that you would like to provide that has not already been covered in other sections?

Yes, I have included several scripts in the folders and want to clarify the location and use for each script:

In summary_statistics_and_visualizations:

new_sum_stat: Visualizations for full datasets and some combined datasets visualizations 

new_dem_sum_stat: Visualizations for demographic datasets that provide information on 'applicants' rather than application. 

In the data_cleaning folder: 

Round_1_2025: Detailed cleaning of variables including standardization of a lot of free text. Creation of demographic datasets.

ami.ipynb: Using HUD API to collect area median income data and categorising applicants into low, very low, extremely low and above low income categories

arcgis.ipynb: Datasets for ArcGIS visualizations and summary statistics for the combined merged dataset.

geocoding.ipynb: Using census API to extract MSA and matched addresses. 

merging.ipynb: This script was used to extract information on bedrooms and age restricted properties by matching addresses across the application datasets and resale transactions datasets. 

2021-2023_Application_Data_Cleaning.ipynb: Initial datacleaning and standardization of the 2021-2023 application dataset

2021-2023_data_cleaning_round2.ipynb: Additional datacleaning and standardization of the 2021-2023 application dataset after geocoding to match addresses and MSAs to property locations occurred

applicant_df.ipynb: Used to create a dataframe containing 1 entry per applicant containing only each applicant's demographic info from their first application for the 2021-2023 application dataset

arcGIS_viz_prep.ipynb: data prep for ArcGIS visualizations

final_standardization.ipynb: standardization of the 2021-2023 and 2023-2025 application datasets to prepare them to be merged

lat_lon_geocoding.ipynb: Geocoding matched property addresses with the census API to match them to latitudes and longitudes.

final_viz_BQ1_BQ2.ipynb: script for the final visualizations created to answer BQ1 and BQ2

The visualizations that we made for the report involved scripts written in python. Those scripts are in the dataset-documentation directories for each of the datasets on the main branch. Similarly, the data cleaning scripts are also in the dataset-documentation directory.
