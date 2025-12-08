
<h1 align="center">
  <br>
  <a href="https://www.bu.edu/spark/" target="_blank"><img src="https://www.bu.edu/spark/files/2023/08/logo.png" alt="BUSpark" width="200"></a>
  <br>
  Citizens’ Housing and Planning Association (CHAPA) – Affordable Housing Applications - Team A
  <br>
</h1>

<h4 align="center">An overview of the repository and its components

<p align="center">
  <a href="#key-components">Key Components</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#project-description">Project Description</a> •
  <a href="#data-locations">Data Locations</a>
</p>

# Project Description

This project is conducted in partnership with **CHAPA (Citizens' Housing and Planning Association)**, Massachusetts’ statewide affordable housing umbrella organization. CHAPA monitors roughly 3,000 permanently affordable homes across the state, and our work contributes to understanding equity and accessibility within the homeownership application process.

### Objective
The goal of this project is to analyze systemic barriers in the application process for permanently affordable homes in Massachusetts. We focus on geographic trends, demographic representation, price sensitivity, and marketing/access disparities to better understand who applies, where they apply, and why certain gaps persist.

### Key Focus Areas
- **Applicant Movement Patterns**: How applicants connect their current residence to the locations of homes they apply for, and how this geographic search radius varies by race, age, household type, and other demographics.
- **Portfolio Bias & Age-Restricted Housing**: To what extent applicant demographics are influenced by CHAPA’s current housing portfolio, which is heavily suburban and often age-restricted.
- **Access & Marketing Disparities**: How listing sources, marketing strategies, and application complexity shape applicant diversity and equitable access.

### Dataset and Prior Work
Our work builds on the **Summer 2025 CHAPA project**, which focused on identifying *what* trends existed in the data. The previous team:
- Used the **Combined Dataset (Merged 2021–2025)** and **Resale Transactions Dataset** from CHAPA.
- Conducted descriptive analyses of age, race/ethnicity, income, assets, household composition, and marketing channels.
- Explored geographic trends and initial impacts of simplifying the application process.
- Examined income and asset gaps and preliminary effects of age-restricted units.

### Current Fall 2025 Scope
The Fall 2025 project shifts toward explaining the *why* and *how* behind these patterns:
- **Integrate four new months of data** into the existing pipeline created by the summer team, following their cleaning and preprocessing documentation.
- Analyze **additional large lottery data**, which may reveal new demographic patterns not visible in the main dataset.
- Consider incorporating external datasets (e.g., **City of Boston** or other monitoring agencies) to broaden geographic and demographic coverage.
- Conduct deeper analysis on:
  - **Movement & Distance**: How far applicants are willing to move and how this varies across demographic groups.
  - **Portfolio Effects**: Distinguishing whether demographic patterns are driven by applicant preferences or CHAPA’s limited property pool.
  - **Price Sensitivity**: Whether maximum resale price influences applicant quantity and demographic composition.
  - **Marketing & Access Disparities**: How different listing sources affect who ends up applying.

This project aims to produce actionable insights for CHAPA that can inform program design, marketing strategy, and policy discussions surrounding equitable access to affordable homeownership opportunities in Massachusetts.
 
# Key Components of our repository
This repository contains all Fall 2025 work for **Team A** within the CHAPA project. 
Below is an overview of the repository structure and key pipeline components, along with short descriptions of what each part of the codebase does. **More detailed documentation for the EDA and Analysis workflow and findings exists within the respective folder’s individual README**.

* `fa25-team-a/data/` – All datasets used in the project  
  - Includes raw and intermediate data files  
  - May require manual download if not stored in the repo

* `fa25-team-a/eda/` – Exploratory Data Analysis notebooks and scripts  
  - Documents data cleaning, preparation, and preliminary visualizations  
  - Contains early insights that informed the modeling process

* `fa25-team-a/analysis/` – Full analytical workflow  
  - Contains scripts and notebooks used to answer all three research questions  
  - Includes modeling, evaluation, and final outputs

* `fa25-team-a/project_definition.md` – Project scope  
  - High-level description of the project goals and guiding questions

* `fa25-team-a/research.md` – Background research  
  - Preliminary research and contextual understanding of the domain
 
# How To Use

To clone and run this application, you'll need <a href="https://git-scm.com" target="_blank">Git</a>
From your command line:


### Clone this repository
```bash
$ git clone https://github.com/BU-Spark/ds-chapa-affordable-housing.git
cd ds-chapa-affordable-housing/fa25-team-a
```
### Set up a virtual environment (Optional)
**Using Conda**
```bash
conda create -n chapa-fa25 python=3.10
conda activate chapa-fa25
```

**Using Python venv**
```bash
python3 -m venv .venv
source .venv/bin/activate     # On macOS/Linux
# OR: .venv\Scripts\activate  # On Windows PowerShell
```

### Installing requirements
```bash
pip install -r requirements.txt
```

# Data locations

Since all of CHAPA's datasets are confidential, below are the attached links to the datasets in the administered access Google Drive.
<a href="dataset-documentation">Dataset Documentation</a>
## Raw Datasets provided by CHAPA
**Applicant datasets**
* CHAPA Chapter 40B Application Data_June 2021 to Sept 2023 - Confidential: [https://docs.google.com/spreadsheets/d/1Bw4DPZ3kvTztUVNY0bQYtYYokJag1XPP/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]
* CHAPA Chapter 40B Application Data_Oct 2023 to May 2025 - Confidential: [https://docs.google.com/spreadsheets/d/1T4fxMvTW0WccmcGBFzH7aLcR0UmW-AAA/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]
*  TOUCHABLE CHAPA Chapter 40B Application Data 2021-2023 & 10_2023-05_2025: [https://docs.google.com/spreadsheets/d/1aOj-mwxEqZFxyOyb-hZ_h4PSL7t55A1B/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]

**Resale Transaction datasets**
*  Resale Transaction Info - Confidential_updated Sept 2025: [https://docs.google.com/spreadsheets/d/1ItkgY49Q_fLOoE0XaJxGXQWfq4kcMFqI/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]
     - Contains transactions updated September 2025
*  TOUCHABLE Resale Transaction Info - Confidential: [https://docs.google.com/spreadsheets/d/1cRnPBugd7m2TfGDZM21ivKTvFtITztui/edit?usp=sharing&ouid=103584276599024109029&rtpof=true&sd=true]
     - PITNE Summer 2025 Team's cleaned transaction data (not updated with September 2025 transactions)

**Price datasets**
* Resale Values_Jun 2021 to Sept 2023: [https://docs.google.com/spreadsheets/d/1gTz3Wg2clVd1Jvw1bTLYa4tanln-FFNs/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]
* Resale Values_Oct 2023 to May 2025: [https://docs.google.com/spreadsheets/d/1Gq_dIYjOjTSYqudI4lqf_mySzj5rOlai/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]
* Resale Values_May 2025 to Sept 2025: [https://docs.google.com/spreadsheets/d/12pygwRwYZ0UKmwyFsNRAOHIgz-H8yrTY/edit?usp=drive_link&ouid=103584276599024109029&rtpof=true&sd=true]
* Property_Data_Jun2021_Sep2025_MissingResaleValues_Completed: [https://drive.google.com/file/d/18OpLHK7w0rI9agJQ25twMncOaTXhNjwg/view?usp=drive_link]
    - Dataset supplied by CHAPA after missing price values were identified during our exploratory data analysis (EDA).

 
 
