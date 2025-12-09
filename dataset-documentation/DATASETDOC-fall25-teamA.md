***Project Information*** 

* What is the project name?

CHAPA Affordable Housing - Team A

* What is the link to your project’s GitHub repository?
[Link](https://github.com/BU-Spark/pitne-affordable-housing-efficacy.git)  
* What is the link to your project’s Google Drive folder? \*\**This should be a Spark\! Owned Google Drive folder \- please contact your PM if you do not have access\*\**
[Link](https://drive.google.com/drive/u/1/folders/1p01teV8XJz43jc-hNAiNo4L22ePyiaex)
* In your own words, what is this project about? What is the goal of this project?

This project analyzes housing application patterns for the Citizens’ Housing and Planning Association (CHAPA), a nonprofit focused on expanding access to affordable housing across Massachusetts. The work uses applicant-level data to understand who applies, where they apply from, and what factors influence their application choices. Overall, the project aims to provide insight into access, equity, and demand in the affordable housing market, helping CHAPA make more informed decisions about property locations, outreach, and policy interventions.
* Who is the client for the project?

David Gasser and Josh Vogel
* Who are the client contacts for the project?

David Gasser: dgasser@chapa.org <br>
Josh Vogel: jvogel@chapa.org
* What class was this project part of?
  
DS701  <br>

***Dataset Information***

* What data sets did you use in your project? Please provide a link to the data sets, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.
[Link](https://drive.google.com/drive/u/1/folders/1nlVp39HIudp6QNPv4IvXQCVbhfo7djES),
[Link](https://drive.google.com/drive/u/1/folders/1iiFpNSMI6VF4kaUujSlOxAJbUot3NVbI)
* Please provide a link to any data dictionaries for the datasets in this project. If one does not exist, please create a data dictionary for the datasets used in this project. **(Example of data dictionary)**

[Link](https://docs.google.com/document/d/11X0lnHchmluo3QoGkTZOfvRwK4fZqhJ4URn9MbBIkuw/edit?tab=t.0)
* What keywords or tags would you attach to the data set?  
  * Domain(s) of Application: Affordable Housing, Housing Applications, Applicant Demographics, Distance to Property, Housing Prices, Portfolio Effects 

*The following questions pertain to the datasets you used in your project.*   
*Motivation* 

* For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description. 

The dataset was created to give CHAPA a clearer understanding of how people interact with the affordable housing system in Massachusetts. By bringing together information on applicant demographics, property characteristics, locations, prices, and application behavior, it fills an important gap in understanding who applies for affordable housing, how far they are willing to move, and what factors shape their choices. The primary purpose was to analyze patterns such as movement distance, demographic differences, the influence of CHAPA’s limited property portfolio, the role of pricing, and how repeat applicants behave compared to one-time applicants. Overall, the dataset was built to support more informed decisions about housing access, equity, and resource planning. <br>

*Composition*

* What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? What is the format of the instances (e.g., image data, text data, tabular data, audio data, video data, time series, graph data, geospatial data, multimodal (please specify), etc.)? Please provide a description.

The instances in this dataset represent individual affordable housing applications submitted to CHAPA. Each row corresponds to a single application and includes information about the applicant (such as age, race, household size, income group), the property they applied to (location, price, unit type), and the applicant’s geographic origin (current address). All datasets were shared as spreadsheets but each instance links applicant characteristics, and property attributes.
* How many instances are there in total (of each type, if appropriate)?
  
The final merged and cleaned dataset we used has 1623 instances.
* Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? If the dataset is a sample, then what is the larger set? Is the sample representative of the larger set? If so, please describe how this representativeness was validated/verified. If it is not representative of the larger set, please describe why not (e.g., to cover a more diverse range of instances, because instances were withheld or unavailable).

The dataset represents a sample of all affordable housing applications submitted across Massachusetts, specifically limited to the properties managed or administered by CHAPA. It is not a complete census of all affordable housing applications statewide, because it only includes applications from CHAPA’s portfolio.
* What data does each instance consist of? “Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description.

Each instance in the dataset consists of structured information describing a single affordable housing application. The data, originally provided as a spreadsheet, includes different parts of the raw administrative records such as applicant demographics, property information, income categories, and prices. These files were cleaned and merged into two datasets; resale and prices data, and applicant data. In addition to the raw application fields, the final dataset also includes features created for analysis, including geocoded coordinates, and calculated distances between applicants and properties. Each instance therefore contains both original raw data and newly crated variables that support movement, pricing, and demographic analyses.
* Is there any information missing from individual instances? If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include redacted text.

Some individual instances in the dataset contain missing information. For example, certain applicant records are missing demographic details such as age, race, or household size. Some property information, such as unit characteristics or specific price information, are also incomplete for a number of applications. This missing information is due to it being unavailable at the time of data collection, such as applicants choosing not to provide certain details or records not being fully entered in the original data files. No data was intentionally removed, and any missing values reflect gaps in the original application records.
* Are there recommended data splits (e.g., training, development/validation, testing)? If so, please provide a description of these splits, explaining the rationale behind them

No formal data splits are provided with this dataset. The dataset is primarily intended for descriptive and exploratory analysis of housing applications rather than for predictive modeling.
* Are there any errors, sources of noise, or redundancies in the dataset? If so, please provide a description.

The dataset contains some sources of noise and potential redundancies. Because the data was collected from multiple data files and merged, there are occasional inconsistencies in formatting, or spelling. Additionally, certain calculated variables, such as distances or geocoded coordinates, may have minor inaccuracies due to approximations or missing address information. Overall, these issues only make up a small amount of noise but do not effect the analytical value of the dataset.
* Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)? If it links to or relies on external resources,   
  * Are there guarantees that they will exist, and remain constant, over time;  
  * Are there official archival versions of the complete dataset (i.e., including the external resources as they existed at the time the dataset was created)?  
  * Are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a dataset consumer? Please provide descriptions of all external resources and any restrictions associated with them, as well as links or other access points as appropriate.

The dataset is self-contained. All information needed for analysis, including applicant demographics, property attributes, pricing, and calculated features such as distances and geocoded coordinates, is included within the dataset itself. It does not link to or rely on external resources such as websites, APIs, or other datasets. There are no dependencies on external data, so there are no guarantees, archival considerations, or restrictions associated with external resources that a dataset consumer would need to consider. All analyses can be performed using the provided data without accessing any outside sources.
* Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)? If so, please provide a description.

The dataset contains confidential and personally identifiable information about applicants, including age, race, household size, income, and current residential address. These details are protected under privacy considerations and cannot be publicly disclosed in a way that would identify individuals.
* Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety? If so, please describe why.

No, the dataset does not contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety. 
* Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset? If so, please describe how.

Since the dataset includes personally identifiable information about applicants, it is possible to indirectly identify individuals from the dataset. 
* Dataset Snapshot, if there are multiple datasets please include multiple tables for each dataset. 
 
| Size of dataset |  |
| :---- | :---- |
| Number of instances | 1623 |
| Number of fields  | 63 |
  
*Collection Process*

* What mechanisms or procedures were used to collect the data (e.g., API, artificially generated, crowdsourced \- paid, crowdsourced \- volunteer, scraped or crawled, survey, forms, or polls, taken from other existing datasets, provided by the client, etc)? How were these mechanisms or procedures validated?

The data was provided by the client. 
* If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deterministic, probabilistic with specific sampling probabilities)?

The dataset represents a sample of CHAPA applications, including all applications received for the properties in the dataset from 2021-2025. The sampling was deterministic, meaning every submitted application for included properties was recorded.
* Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent crawl of old news articles)? If not, please describe the timeframe in which the data associated with the instances was created.
 
Data was collected from 2021-2025. The data corresponds to the dates of application submissions and property transactions, so the timeframe of data collection aligns closely with the creation timeframe of the individual application instances. <br> 

*Preprocessing/cleaning/labeling* 

* Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? If so, please provide a description. If not, you may skip the remaining questions in this section.

The dataset underwent preprocessing and cleaning after being provided by the client. Steps included standardizing categorical fields such as race, restricted property, household type, and application source to ensure consistency, processing missing values by either leaving them blank, imputing median, or removing incomplete records.
* Were any transformations applied to the data (e.g., cleaning mismatched values, cleaning missing values, converting data types, data aggregation, dimensionality reduction, joining input sources, redaction or anonymization, etc.)? If so, please provide a description.

Fields such as age, price, and address were converted for more consistent formats. We merged all data files from the client into one dataset that included our geocoded addition to the data. 
* Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? If so, please provide a link or other access point to the “raw” data, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.

The "raw" data was saved separately to support reproducibility and potential future analyses. Access to these "raw" files is not publicly available.
* Is the code that was used to preprocess/clean the data available? If so, please provide a link to it (e.g., EDA notebook/EDA script in the GitHub repository).

The code used for preprocessing and cleaning, including merging files, standardizing fields, and calculating derived features, is maintained in our project notebooks. These notebooks can be found on team’s GitHub repository. <br> 

*Uses* 

* What tasks has the dataset been used for so far? Please provide a description.

* The dataset has been used for several descriptive and exploratory analyses. This includes movement and distance analysis, examining how far applicants apply from their current residence and whether this varies by race, age, or household characteristics. It has also been used to study portfolio effects, investigating the extent to which applicant demographics are influenced by the limited number of CHAPA properties versus applicant choice. Analyses of price effects have examined how the maximum resale price of affordable homes affects the number of applicants and their demographics while controlling for income limits. Finally, repeat versus non-repeat applicant analyses explored differences in demographics between applicants who apply multiple times versus one-time applicants, as well as whether they apply to similar or nearby properties.
* What (other) tasks could the dataset be used for?

The dataset could be used for predictive modeling, such as forecasting applicant demand for specific properties or identifying factors associated with repeat applications. It could also support policy analysis, including evaluating equity in access to affordable housing across demographic groups or analyzing trends in property pricing and resale data.
* Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?

Derived features and cleaned fields, such as distances, race categories, and geocoded coordinates, reflect preprocessing decisions that could affect analyses that require alternative representations.
* Are there tasks for which the dataset should not be used? If so, please provide a description.

The dataset should not be used to publicly identify individuals, as it contains personally identifiable information. It is also not appropriate for tasks that require a complete or fully representative sample of all affordable housing applicants in Massachusetts, because it only includes CHAPA properties. <br>

*Distribution*

* Based on discussions with the client, what access type should this dataset be given (eg., Internal (Restricted), External Open Access, Other)?

Based on discussions with the client, the dataset should be classified as Internal (Restricted). It contains personally identifiable information, including current addresses, age, and household characteristics, so access should be limited to authorized personnel only. <br>

*Maintenance* 

* If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? If so, please provide a description.

At this time, there is no formal mechanism for other users to extend or contribute to the dataset. Updates or augmentations are managed internally by the project team in coordination with the client. Any future contributions or extensions would require approval and careful review to maintain data privacy and consistency. <br>

*Other*

* Is there any other additional information that you would like to provide that has not already been covered in other sections?

It is important to not that the dataset is highly structured and cleaned for analysis, including derived features. It does not represent the full population of affordable housing applicants in Massachusetts, so analyses should take this limitation into account. Users should also follow all privacy and data protection guidelines when working with this dataset.
