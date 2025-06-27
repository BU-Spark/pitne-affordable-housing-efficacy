***Project Information*** 

* What is the project name?
Team CHAPA - Improving Access to Affordable Homeownership

* What is the link to your project’s GitHub repository?
[Link](https://github.com/BU-Spark/pitne-affordable-housing-efficacy.git)

* What is the link to your project’s Google Drive folder? \*\**This should be a Spark\! Owned Google Drive folder \- please contact your PM if you do not have access\*\**  
[Link](https://drive.google.com/drive/folders/1OhYmg-8f7ar-rGoFBal5h7by8BbwKDbe?usp=drive_link)

* In your own words, what is this project about? What is the goal of this project?   
To support CHAPA with expanding access to homeownership for low-income and underrepresented families by highlighting trends in application data and examining how systems impact who applies and who is excluded.

* Who is the client for the project?  
CHAPA: Citizens’ Housing and Planning Association

* Who are the client contacts for the project?  
David Gasser

* What class was this project part of?
PIT-NE Impact Tech Fellowship Summer 2025


***Dataset Information***
* What data sets did you use in your project? Please provide a link to the data sets, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.  
N/A - Datasets are confidential to our client. We used three datasets. One for Resale Transaction Information from the past 4 years of sales. Two for application data.
  
* What keywords or tags would you attach to the data set?  
  * Domain(s) of Application: Civic Tech, Housing, Affordable Homeownership, Policymaking


*The following questions pertain to the datasets you used in your project.*   
*Motivation* 

* For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description. 
The datasets were created for data analysis during this project.  

*Composition*

* What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? What is the format of the instances (e.g., image data, text data, tabular data, audio data, video data, time series, graph data, geospatial data, multimodal (please specify), etc.)? Please provide a description. 

The datasets were shared in thr form of spreadsheets. They contain application information and resale information. All of the rows are anonymized using Applicant IDs.

* Is there any information missing from individual instances? If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include redacted text.  
The first dataset is missing some information that the second dataset contains. This is just by virtue of the application process changing between the collection of the datasets.
 
* Are there any errors, sources of noise, or redundancies in the dataset? If so, please provide a description.   
There were some missing values in the Start Dates and Closing Dates. These were confirmed with the client. There were some missing values for the properties listed and up to date information was sourced form online listings after approval from our client. 


| Size of dataset |158 rows  |
| Number of fields  |6 columns|

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

---
- All scripts were committed to the appropriate **GitHub branch**. 

* Is the code that was used to preprocess/clean the data available? If so, please provide a link to it (e.g., EDA notebook/EDA script in the GitHub repository). 
Yes, here is the link - (https://github.com/BU-Spark/pitne-affordable-housing-efficacy/tree/2a31fd08cb0b78e8de609454c869144481083cde/dataset-documentation/data-cleaning-scripts)[Link]


*Uses* 

* What tasks has the dataset been used for so far? Please provide a description.   
Data analysis -> Visualizations for our report and for our presentations

* Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?   
It is confidential.

* Are there tasks for which the dataset should not be used? If so, please provide a description.


*Distribution*

* Based on discussions with the client, what access type should this dataset be given (eg., Internal (Restricted), External Open Access, Other)?
Our datasets are intended to be confidential and remain internal with our client. 

*Maintenance* 

* If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? If so, please provide a description. 

N/A - Datasets are confidential to our client.

*Other*

* Is there any other additional information that you would like to provide that has not already been covered in other sections?

The visualizations that we made for the report involved scripts written in python. Those scripts are in the dataset-documentation directories for each of the datasets on the main branch. Similarly, the data cleaning scripts are also in the dataset-documentation directory.
