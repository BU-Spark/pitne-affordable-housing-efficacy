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

## 1. Missing Bedroom Information
- Searched online for the number of bedrooms for 4 properties maintained by **CHAPA** that were missing this data.

## 2. Sorting and Download
- Sorted the sheet by **Transaction Start Date**.
- Downloaded the spreadsheet for **Round 2**.

## 3. Date Column Conversion
- Changed **Start Date** and **Closing Date** columns from string objects to datetime format for efficient processing.

## 4. Transaction Filtering Script
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

## 5. Age Restricted Column Standardization
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

## 6. Geocoding Process

### Preparation
- Sorted sheet by **Town** for easier review.
- Created a plan:
  - Prepare imports and DataFrame.
  - Add a **Unique ID** column to the CSV as required by the census geocoder API.
  - Use **batch geocoding** to obtain standardized addresses.

### MSA Matching
- Accessed corresponding MSAs **row by row**.
- Created a new DataFrame with the following new columns:
  - `Match Status`
  - `Match Type`
  - `Matched Address`

### Manual Review
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
