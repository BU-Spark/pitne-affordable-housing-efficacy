
<h1 align="center">
  <br>
  <a href="https://www.bu.edu/spark/" target="_blank"><img src="https://www.bu.edu/spark/files/2023/08/logo.png" alt="BUSpark" width="200"></a>
  <br>
  CHAPA Affordable Housing Project
  <br>
</h1>

<h4 align="center">A repo providing a data analysis of CHAPA's application data. </h4> <change to repo short description>

<p align="center">
  <a href="#project-description">Project Description</a> •
  <a href="#How To Use">How To Use</a> •
  <a href="#chapa--local-data-access">CHAPA - Local Data Access</a> •
  <a href="#folder-structure-guide">Folder Structure Guide</a> 
</p>

# Project Description

The purpose of this project is to **assist the Citizens’ Housing and Planning Association (CHAPA)** with demographic information regarding applicants to their affordable housing projects.  
With a portfolio of nearly **3,000 properties**, CHAPA has a wide range of applicants — both from within Massachusetts and out-of-state individuals.

Continuing the work of students in the **Summer of 2025**, we are focusing on identifying **applicant movement patterns**, **portfolio biases**, and the **importance of age-restricted home offerings**.

---

### The project is divided into three main base questions:

#### **1. Movement & Distance Analysis**
- Identifying movement patterns of applicants  
- Do applicants apply to properties around their current residence?  
- Are they applying solely to major cities?  
- Are locations of applicants static or showing changing trends?  

---

#### **2. Geographical Range Analysis**
- Are applicants applying to properties regardless of location?  
- Are there specific regions with high/low applicant interest?  
- What regions or major cities are out-of-state applicants applying to?  

---

#### **3. Portfolio Effects**

**Demographic Influence**
- What factors are influencing the varying demographics of applicants?  
- Are there any specific demographic trends?  
- Considerations include: race/ethnicity, age, current residence, household income, and household assets  

**Price**
- Price deterring applicants?  
- Does property price affect applicant quantity?  
- Are these demographic trends different for lower vs. higher-priced properties?

# CHAPA – Local Data Access


This repo uses **Google OAuth (per user)** to read files from the shared Drive folder named **`Dataset`**. Data is downloaded to `data/` (gitignored). Secrets are kept out of Git.

---
## 🚀 How To Use

This guide explains how to set up the environment, configure Google OAuth,
place data correctly, and run the full CHAPA Team B processing pipeline.

---

### 1. Clone the repository

```bash
git clone https://github.com/BU-Spark/ds-chapa-affordable-housing.git
cd ds-chapa-affordable-housing/fa25-team-b
```

---

### 2. (Optional) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 4. Google OAuth Setup (Required for Sheets-Based Scripts)

Some validation scripts connect to Google Sheets (crosswalks, validation tables).
These require Google OAuth credentials.

### 4.1 Create OAuth Credentials

🟩 Visit: https://console.cloud.google.com  
🟩 Go to **APIs & Services → Credentials**  
🟩 Click **Create Credentials → OAuth Client ID**  
🟩 Choose **Desktop App**  
🟩 Download the JSON file  
🟩 Save it to:

```
fa25-team-b/.credentials/client_secret.json
```

*(Create the `.credentials/` folder if it does not exist.)*

---

### 4.2 First-Time Google Authentication

🟩 Run any script that uses Google Sheets  
🟩 A browser window will open  
🟩 Log in with your BU Google account  
🟩 Approve access  

A token file will be created:

```
fa25-team-b/.credentials/token.json
```

---

## 📁 5. Data Locations

Raw CHAPA CSV files (confidential):

```
data/raw/
```

Outputs created by scripts:

```
data/processed/
data/cache/
```

Notebooks and visuals:

```
notebooks/
visuals/
```

---

## ⚙️ 6. Run the Data Processing Pipeline

Run all cleaning + property extraction + geocoding scripts from the
`fa25-team-b` directory.

---

### 6.1 Clean application-level data

```bash
python cleaners/01_clean_applications.py
```

Produces:

🟩 `data/processed/applications_clean.parquet`

---

### 6.2 Extract unique CHAPA properties

```bash
python cleaners/07_find_chapa_properties.py
```

Produces:

🟩 `data/processed/chapa_properties_from_apps.csv`

---

### 6.3 Geocode CHAPA properties (cached)

```bash
python cleaners/08_geocode_chapa_properties.py
```

Produces:

🟩 `data/cache/property_geocode.parquet`  
🟩 `data/processed/applications_with_property_geo.parquet`

---


## Pipeline
You can run all the scripts in order if you wish, but the only important ones are number 4 and number 6. Files land in `data/` and are **not** committed to Git.  

---


## 📁 Data Locations

The CHAPA project relies on **confidential raw datasets** stored in a private
Google Drive folder. These files are **never committed to GitHub** and are
pulled locally using OAuth through the scripts in `fa25-team-b/scripts`.

Below is a complete map of where data lives inside the `fa25-team-b` folder.

CHAPA application data is confidential and therefore not available on this public repo. We have worked around this using OAuth; go back to the Local Data Access section for more information. Beyond that, here is a breakdown of what belongs in each folder and what each file does.

<a href="dataset-documentation">Dataset Documentation</a>

### 🧩 `assets/`
Contains static reference files and lookup tables used to support cleaning and analysis.  
- Example: `city_names_norm_ma.csv` — standardized list of Massachusetts city names used for matching and geographic encoding.  
- These files do not change frequently and are used by scripts in `cleaners/` or `tools/`.

---

### 🧹 `cleaners/`
Contains all **data-cleaning and preprocessing scripts** that prepare the raw CHAPA dataset for analysis.  
Each script focuses on a specific aspect of the cleaning pipeline.

#### **`HUD_economic_data_import_cleaning.py`**
- Imports, cleans, and appends **Multifamily Tax Subsidy (MTSP) Income Limit data** from HUD to the applicant dataset.  
- Ensures consistent linkage between applicant income levels and federal HUD thresholds.  

#### **`append_resale_data.py`**
- Takes the application dataset and **appends resale value datasets** to it.  
- Integrates resale-related attributes to allow further analysis on property affordability and pricing trends.  

#### **`current_residence_name_normalization_v1.py`**
- Normalizes the **‘Current Residence’** column in the application dataset.  
- Handles directional abbreviations (e.g., *N.*, *S.*, *E.*, *W.* → *North*, *South*, *East*, *West*).  
- Merges subregions (e.g., *East Boston*, *West Boston* → *Boston*).  
- Applies **fuzzy matching** against a standardized list of Massachusetts city names.  

#### **`geographic_encoding_ma_cities.py`**
- Geolocates normalized city names for spatial analysis.  
- Outputs columns for `city_name`, `longitude`, `latitude`, and `full_location_name`.  
- Enables visualization of applicant distributions across Massachusetts.  

#### **`race_naming_normalization.py`**
- Normalizes the **‘Race/Ethnicity’** column in the dataset.  
- Fixes symbol issues, typos, and inconsistent abbreviations.  
- Creates a **‘White_MENA’** category and adds **dummy columns** for each race.  
- Adds a boolean **`is_mixed_race`** column to flag multi-racial applicants.  
- Final standardized race field is stored in `race_norm_final`.  

#### **`race_norm_corrections.py`**
- Performs **secondary corrections** on the race column after normalization.  
- Combines “unknown” and “choose_not_to_answer” responses.  
- Fixes logic where “White_MENA” was incorrectly included in other race flags.  
- Recreates dummy columns to ensure clean final outputs.  


---

### ⚙️ `config/`
Stores configuration files that define reusable project parameters.  
These YAML files centralize column names, dataset references, and schema mappings.  
- **`columns.yaml`** → maps raw dataset column names to standardized labels.  
- **`datasets.yaml`** → specifies dataset paths, descriptions, and metadata.  
These files ensure reproducibility across different scripts and notebooks.

---

### 📊 `data/`
Used to store local or intermediate datasets.  
- Contains cleaned `.csv` or `.parquet` files created during preprocessing.  
- **Raw CHAPA data is *not* stored here** due to confidentiality — it’s instead accessed from a secure Google Drive folder.  
- Temporary or test data (like `temp.txt`) may also appear here during development.

---

### 📚 `docs/`
Contains all written documentation related to the project.  
- **`project_definition.md`** → outlines project goals, scope, and deliverables.  
- **`research.md`** → captures contextual background, references, and insights from literature or external data.  
This folder serves as the central repository for explanatory materials and reporting.

---

### 🔍 `eda/` (Exploratory Data Analysis)
Includes scripts and notebooks used for exploration, visualization, and data insight generation.  
- **`age_eda.py`** → analyzes age-restricted properties and applicant demographics.  
- **`CHAPA_TeamB_EDA.ipynb`** → main exploratory notebook for all visual and statistical summaries.  
- **`CHAPA_TeamB_EDA_2nd_version.ipynb`** → updated version incorporating refined plots and metrics.  
All EDA outputs (figures, charts) are automatically saved to the `visuals/` folder.

---

### 🧮 `scripts/`
Automation and pipeline scripts that connect to the CHAPA data sources, perform cleaning, and orchestrate workflows.  
These are generally executed in sequence to fetch, clean, and prepare data for analysis.  
- **`01_auth.py`** → authenticates access to CHAPA / Google Drive data.  
- **`03_pull_dataset.py` / `04_pull_all.py`** → download and combine raw data.  
- **`05_clean_pipeline.py` / `06_clean_applications_pipeline.py`** → run full cleaning workflows.    
Together, these scripts automate the end-to-end data preparation process. Unnumbered scripts exist for data analysis:
- **`analyze_property_popularityV2.py`** → analyzes property-level application demand.

---

### 🧰 `tools/`
Utility scripts that provide helper functions used across multiple modules.  
- **`google_drive.py`** → handles Drive API operations for data import/export.  
- **`schema.py`** → manages dataset schema consistency and validation.  
This folder helps modularize shared functionality, keeping the main scripts cleaner.

---

### 📈 `visuals/`
Contains all visualization outputs produced from EDA scripts and notebooks.  
- Stores static plots (`.png`), interactive charts (`.html`), and categorized folders for specific analyses.  
- Example files:  
  - `applications_map.html` → interactive map of housing applications.  
  - `applications_pareto.png`, `applications_vs_price_binned.png` → visual summaries of property demand and affordability.  
  - `top_properties_bar.png`, `top_properties_stacked.png` → visual comparisons of top housing properties.  
- Subfolders:  
  - **`Age Restricted Analysis/`** → visuals focusing on senior/age-restricted properties.  
  - **`Income and Demographics vs Applications/`** → plots exploring socioeconomic and demographic patterns.  

---
