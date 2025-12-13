
<h1 align="center">
  <br>
  <a href="https://www.bu.edu/spark/" target="_blank"><img src="https://www.bu.edu/spark/files/2023/08/logo.png" alt="BUSpark" width="200"></a>
  <br>
  CHAPA Affordable Housing Project
  <br>
</h1>

<h4 align="center">Geospatial and demographic analysis of CHAPA affordable housing applications across Massachusetts</h4>

<p align="center">
  <a href="#project-description">Project Description</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#google-oauth-setup">Google OAuth Setup</a> •
  <a href="#run-the-data-processing-pipeline">Run Pipeline</a> •
  <a href="#key-outputs">Key Outputs</a> •
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

---

## How To Use

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

## Google OAuth Setup

Our data is located in a shared google folder, and is confidential. Since we cannot have our data shared publicly, we are using **Google OAuth** to access data from our drives locally. This works for anyone who has sharing access to the dataset folder, as long as you obtain the necessary JSON from a team member.

### 4.1 Get JSON setup

- Get the oauth_client.json file from a team member
- Save it to:

```
fa25-team-b/secrets/client_secret.json
```

Create the `secrets/` folder if it does not exist. Folders with this name are gitignored.

If you are unable to contact a team member or want to set up OAuth for yourself, you can do so [here.](https://console.cloud.google.com/apis). Simply create a new OAuth project, setting it up as you would for a desktop app. Once you've generated the necessary JSON, do the same as above.

---

### 4.2 First-Time Google Authentication

- Run script 01_oauth.py
- A browser window will open  
- Log in with your BU Google account  
- Approve access  

A token file will be created:

```
fa25-team-b/secrets/token.json
```
This is all you have to do. You never have to rerun this script -- as long as the token is cached, your repository will have access to your google account, and therefore be able to pull the necessary files. This is done using scripts 04_pull_all.py.

---

## Data Locations

Once pulled, the raw CHAPA CSV files will land in the raw folder:

```
data/raw/
```
The entire data folder is gitignored, so don't worry about accidentally uploading confidential data.

Data cleaning scripts also use these folders:
```
data/processed/
data/cache/
data/interim
```
Folders are created if they don't already exist.

Visuals produced by scripts land here:

```
visuals/
```

---

## Run the Data Processing Pipeline

The easiest way to run the complete pipeline is to use the automated script:

```bash
./run_data_pipeline.sh
```

This script runs five key steps:
1. **Pulls data from Google Drive** (`scripts/04_pull_all.py`)
2. **Cleans application data** (`scripts/06_clean_applications_pipeline.py`)
3. **Generates static visualizations** (`scripts/popularity_graph_generation.py`)
4. **Generates age-restricted analysis** (`scripts/age_analysis.py`)
5. **Generates interactive map** (`scripts/folium_map_generation.py`)

---

### What the Pipeline Does

#### Step 1: Pull Data (`04_pull_all.py`)
- Downloads raw CHAPA datasets from Google Drive
- Saves to `data/raw/`
- Uses OAuth credentials from Step 4

#### Step 2: Clean Applications (`06_clean_applications_pipeline.py`)
- Loads and standardizes column headers
- Normalizes current residence using fuzzy matching
- Geocodes applicant locations
- Normalizes race/ethnicity data
- Appends resale price data
- Appends HUD MTSP income limit data
- Geocodes property locations
- Produces: `data/processed/applications_clean.parquet`

#### Step 3: Generate Static Visualizations (`popularity_graph_generation.py`)
- Creates price vs. application volume analysis
- Generates top properties bar charts (overall and by demographics)
- Produces Pareto chart showing application concentration
- Analyzes 11 comprehensive traits of most popular properties including:
  - Property characteristics (price)
  - Distance metrics (median, average)
  - Applicant demographics (age, household size, dependents)
  - Financial characteristics (income, assets)
  - Special status (disability, first-time homebuyer)
- Produces:
  - `visuals/Portfolio Effects Analysis/applications_vs_price_binned.png`
  - `visuals/Portfolio Effects Analysis/top_properties_bar.png`
  - `visuals/Portfolio Effects Analysis/top_properties_stacked.png`
  - `visuals/Portfolio Effects Analysis/applications_pareto.png`
  - `visuals/Portfolio Effects Analysis/trait_comparison_*.png` (11 individual trait visualizations)
  - `visuals/Portfolio Effects Analysis/popular_property_traits_analysis.csv`
  - `visuals/Portfolio Effects Analysis/property_demand_with_geo.csv`

#### Step 4: Generate Age-Restricted Analysis (`age_analysis.py`)
- Analyzes age-restricted (55+/62+) properties and applicant demographics
- Creates age distribution visualizations
- Compares age-restricted vs. non-age-restricted properties
- Analyzes income and race patterns by age group
- Produces:
  - `visuals/Age Restricted Analysis/age_distribution_all.png`
  - `visuals/Age Restricted Analysis/age_distribution_unique.png`
  - `visuals/Age Restricted Analysis/age_restricted_vs_nonrestricted.png`
  - `visuals/Age Restricted Analysis/race_distribution_by_restriction_top.png`
  - `visuals/Age Restricted Analysis/applications_per_property_horizontal.png`
  - `visuals/Age Restricted Analysis/income_by_agebin.png`
  - `visuals/Age Restricted Analysis/heatmap_age_vs_race_restricted_clean.png`

#### Step 5: Generate Interactive Map (`folium_map_generation.py`)
- Creates enhanced geospatial visualization
- Includes demographic heatmaps, property markers, and flow analysis
- Produces: `visuals/Portfolio Effects Analysis/applications_map_enhanced.html`

---

### Manual Execution

If you prefer to run steps individually:

```bash
# Step 1: Pull data
PYTHONPATH=. python scripts/04_pull_all.py

# Step 2: Clean data
PYTHONPATH=. python scripts/06_clean_applications_pipeline.py

# Step 3: Generate static visualizations (outputs to Portfolio Effects Analysis by default)
python scripts/popularity_graph_generation.py --input data/processed/applications_clean.parquet

# Step 4: Generate age-restricted analysis
python scripts/age_analysis.py --input data/processed/applications_clean.parquet --outdir "visuals/Age Restricted Analysis"

# Step 5: Generate interactive map (outputs to Portfolio Effects Analysis by default)
python scripts/folium_map_generation.py --input data/processed/applications_clean.parquet
```

---

## Key Outputs

After running the pipeline, you'll have:

### 📊 Cleaned Data
- `data/processed/applications_clean.parquet` — Fully processed application dataset with geocoding, normalized demographics, and property information

### 🗺️ Interactive Visualizations
- `visuals/Portfolio Effects Analysis/applications_map_enhanced.html` — Interactive map with demographic heatmaps, property markers, distance analysis, and applicant flow patterns

### 📈 Portfolio Effects Analysis
All portfolio analysis outputs are in `visuals/Portfolio Effects Analysis/`:

**Static Charts:**
- `applications_pareto.png` — Pareto chart showing application concentration
- `applications_vs_price_binned.png` — Demand vs. price analysis
- `top_properties_bar.png` — Top properties by application count
- `top_properties_stacked.png` — Demographic breakdown by property

**Trait Comparison Visualizations** (11 individual analyses):
- `trait_comparison_price.png` — Maximum resale price comparison
- `trait_comparison_distance_median.png` — Median applicant distance
- `trait_comparison_distance_avg.png` — Average applicant distance
- `trait_comparison_age_mean.png` — Mean applicant age
- `trait_comparison_hh_size_mean.png` — Mean household size
- `trait_comparison_dependents_mean.png` — Mean number of dependents
- `trait_comparison_hh_income_median.png` — Median household income
- `trait_comparison_hh_assets_median.png` — Median household assets
- `trait_comparison_hh_assets_mean.png` — Mean household assets
- `trait_comparison_disability_pct.png` — Proportion with disability
- `trait_comparison_fthb_pct.png` — Proportion first-time homebuyers

**Data Exports:**
- `property_demand_with_geo.csv` — Property-level demand data with coordinates
- `popular_property_traits_analysis.csv` — Statistical analysis comparing popular vs. all properties across 16 traits

### 📓 Analysis Notebooks
- `eda/CHAPA_TeamB_EDA.ipynb` — Main exploratory data analysis
- `eda/CHAPA_TeamB_EDA_2nd_version.ipynb` — Updated EDA with refined visualizations
- `eda/Bayesian_Model.ipynb` — Bayesian statistical modeling of application patterns

---

## Folder Structure Guide

The CHAPA project relies on **confidential raw datasets** stored in a private
Google Drive folder. These files are **never committed to GitHub** and are
pulled locally using OAuth through the scripts in `fa25-team-b/scripts`. Below is a breakdown of what belongs in each folder and what each file does.

### 🧩 `assets/`
Contains static reference files and lookup tables used to support cleaning and analysis.  
- Example: `city_names_norm_ma.csv` — standardized list of Massachusetts city names used for matching and geographic encoding.  
- These files do not change frequently and are used by scripts in `cleaners/` or `tools/`.


---


### 🧹 `cleaners/`
Contains all **data-cleaning and preprocessing scripts** that prepare the raw CHAPA dataset for analysis.
Each script focuses on a specific aspect of the cleaning pipeline and is called by `scripts/06_clean_applications_pipeline.py`.

#### **`HUD_economic_data_import_cleaning.py`**
- Imports, cleans, and appends **Multifamily Tax Subsidy Program (MTSP) Income Limit data** from HUD
- Links applicant income levels to federal HUD income thresholds
- Enables affordability eligibility analysis

#### **`append_resale_data.py`**
- Appends **resale value datasets** to the application data
- Integrates property pricing information for affordability and demand analysis

#### **`current_residence_name_normalization_v1.py`**
- Normalizes the **'Current Residence'** column using fuzzy matching
- Handles directional abbreviations (e.g., *N.*, *S.*, *E.*, *W.* → *North*, *South*, *East*, *West*)
- Merges subregions (e.g., *East Boston*, *West Boston* → *Boston*)
- Matches against standardized Massachusetts city names from `assets/city_names_norm_ma.csv`

#### **`geographic_encoding_ma_cities.py`**
- Geocodes normalized city names for spatial analysis
- Uses Nominatim geocoding with local caching to avoid redundant API calls
- Outputs `city_name`, `longitude`, `latitude`, and `full_location_name`
- Enables mapping and distance calculations

#### **`applicant_property_geocoding.py`**
- Geocodes property addresses for accurate map placement
- Calculates distances between applicant locations and properties
- Uses Haversine formula for great-circle distance calculations
- Caches results in `data/cache/` to improve performance

#### **`race_naming_normalization.py`**
- Normalizes the **'Race/Ethnicity'** column in the dataset
- Fixes symbol issues, typos, and inconsistent abbreviations
- Creates **'White_MENA'** category (Middle Eastern/North African)
- Adds **dummy columns** for each race category
- Adds boolean **`is_mixed_race`** column to flag multi-racial applicants
- Produces `race_norm_final` standardized field

#### **`race_norm_corrections.py`**
- Performs **secondary corrections** on race normalization
- Combines "unknown" and "choose_not_to_answer" responses
- Fixes logic where "White_MENA" was incorrectly included in other race flags
- Recreates dummy columns to ensure clean final outputs

#### **`geocode_utils.py`**
- Normalizes input address strings before lookup
- Implements in-memory caching to avoid duplicate API requests
- Includes rate-limit–safe request handling for batch geocoding
- Returns clean coordinate pairs (latitude, longitude) for both applicant origins and property destinations

#### **`distance_utils.py`**
- Implements the Haversine great-circle distance formula
- Computes straight-line geographic distance between coordinate pairs
- Returns distances in kilometers (with miles conversion handled upstream)

#### **`compute_distances.py`**
- Uses geocode_utils.py for Google API geocoding with caching
- Computes great-circle distances between applicant origins and property coordinates
- Appends latitude, longitude, and distance fields to the dataset
- Outputs data/with_distance.csv for use in movement analysis, KDE plots

---

### ⚙️ `config/`
Stores configuration files that define reusable project parameters.  
These YAML files centralize column names, dataset references, and schema mappings.  
- **`columns.yaml`** → maps raw dataset column names to standardized labels.  
- **`datasets.yaml`** → specifies dataset paths, descriptions, and metadata.  
These files ensure reproducibility across different scripts and notebooks.

---

### 📊 `data/`
Local data storage for raw, interim, processed, and cached datasets.
**All contents are gitignored** to protect confidential CHAPA data.

#### **Subdirectories**
- **`data/raw/`** — Raw datasets downloaded from Google Drive (never committed to Git)
- **`data/interim/`** — Intermediate outputs during cleaning pipeline
- **`data/processed/`** — Final cleaned datasets (e.g., `applications_clean.parquet`)
- **`data/cache/`** — Cached geocoding results and computed data to avoid redundant API calls
  - `geocode.parquet` — Cached city geocodes
  - `property_geocode.parquet` — Cached property coordinates

Raw CHAPA data is **never** stored in the repository — it's accessed securely from Google Drive using OAuth.

---

### 📚 `docs/`
Contains all written documentation related to the project.  
- **`project_definition.md`** → outlines project goals, scope, and deliverables.  
- **`research.md`** → captures contextual background, references, and insights from literature or external data.  
This folder serves as the central repository for explanatory materials and reporting.

---

### 🔍 `eda/` (Exploratory Data Analysis)
Jupyter notebooks and scripts for data exploration, statistical analysis, and insight generation.

- **`CHAPA_TeamB_EDA.ipynb`** — Main exploratory notebook covering:
  - Application trends over time
  - Age distribution analysis
  - Household income and assets analysis
  - Race/ethnicity demographics
  - Income vs. resale value relationships

- **`CHAPA_TeamB_EDA_2nd_version.ipynb`** — Updated EDA with:
  - Refined visualizations
  - Additional statistical summaries
  - Improved demographic breakdowns

- **`Bayesian_Model.ipynb`** — Bayesian statistical modeling including:
  - Hierarchical models for application patterns
  - Probabilistic analysis of demographic influences
  - Inference on property preferences and accessibility

- **`age_eda.py`** — Original age analysis script (legacy):
  - Reads from Excel file directly
  - Now superseded by `scripts/age_analysis.py` which integrates with the pipeline
  - Kept for reference and manual analysis

All EDA outputs (figures, charts) are saved to the `visuals/` folder and subfolders.

---

### 🧮 `scripts/`
Automation and pipeline scripts that connect to CHAPA data sources, perform cleaning, and generate visualizations.
These scripts orchestrate the end-to-end workflow from data acquisition to analysis outputs.

#### **Pipeline Scripts (numbered, run in order)**
- **`01_auth.py`** — Authenticates Google OAuth for Drive access (run once during setup)
- **`02_list_datasets.py`** — Lists available datasets in the Google Drive folder
- **`03_pull_dataset.py`** — Downloads a single dataset from Google Drive
- **`04_pull_all.py`** — Downloads all datasets from Google Drive (used in pipeline)
- **`05_clean_pipeline.py`** — Legacy cleaning orchestrator
- **`06_clean_applications_pipeline.py`** — Main cleaning pipeline (calls all cleaners, produces `applications_clean.parquet`)

#### **Analysis & Visualization Scripts**
- **`age_analysis.py`** — Generates comprehensive age-restricted property analysis (55+/62+ properties, age demographics, income patterns)
- **`folium_map_generation.py`** — Generates enhanced interactive map with demographic layers, property markers, and heatmaps
- **`popularity_graph_generation.py`** — Creates static charts analyzing property popularity and demand patterns
- **`analyze_property_popularityV2.py`** — Legacy analysis script (V2, superseded by popularity_graph_generation.py)
- **`geocode_properties_for_map.py`** — Geocodes property addresses for map visualization

---

### 🧰 `tools/`
Utility scripts that provide helper functions used across multiple modules.  
- **`google_drive.py`** → handles Drive API operations for data import/export.  
- **`schema.py`** → manages dataset schema consistency and validation.  
This folder helps modularize shared functionality, keeping the main scripts cleaner.

---

### 📈 `visuals/`
All visualization outputs produced from EDA scripts and notebooks.
Includes static plots (`.png`), interactive maps (`.html`), and CSV exports.

#### **Subfolders**

- **`Portfolio Effects Analysis/`** — Comprehensive property popularity and demand analysis:
  - **Interactive Map:** `applications_map_enhanced.html` — Enhanced geospatial visualization with demographic heatmaps, property markers, distance metrics, flow analysis, and interactive filters
  - **Static Charts:** Price vs. demand, top properties (overall and by demographics), Pareto concentration chart
  - **Trait Comparisons:** 11 individual visualizations comparing popular vs. unpopular properties across:
    - Property characteristics (price)
    - Distance metrics (median/average applicant distance)
    - Demographics (age, household size, dependents)
    - Financial (income, assets)
    - Special status (disability, first-time homebuyer)
  - **Data Exports:** Property demand with coordinates, statistical trait analysis CSV

- **`Age Restricted Analysis/`** — Visualizations for senior (55+/62+) properties:
  - Age distribution analysis
  - Income and asset patterns by age group
  - Race/ethnicity comparisons
  - Applications per age-restricted property

- **`Income and Demographics vs Applications/`** — Socioeconomic and demographic analysis:
  - Income distribution by property type
  - Applicant count vs. median income
  - Race/ethnicity composition by property
  - Applications vs. household assets

See `visuals/README.md` for detailed descriptions of all visualizations.

---

## 📚 Additional Documentation

Beyond this main README, the repository includes folder-specific documentation:

- **`visuals/README.md`** — Overview of the folder and visualizations.
- **`visuals/Portfolio Effects Analysis/README.md`** — Detailed explanation of portfolio effects visualizaion outputs
- **`visuals/Income and Demographics vs Applicants Analysis/README.md`** — Detailed explanation of income/demographics graphs
- **`eda/README.md`** — Overview of exploratory data analysis notebooks and methodology

---

## 🛠️ Dependencies

The project uses Python 3.8+ with the following key packages (see `requirements.txt` for complete list):

### **Data Processing**
- `pandas` — Data manipulation and analysis
- `numpy` — Numerical operations
- `pyarrow` — Parquet file support

### **Geocoding & Geospatial**
- `geopy` — Geocoding via Nominatim
- `geopandas` — Geographic data processing
- `shapely` — Geometric operations
- `pyproj` — Coordinate system transformations

### **Visualization**
- `matplotlib` — Static plotting
- `folium` — Interactive maps
- `tqdm` — Progress bars

### **String Matching**
- `rapidfuzz` — Fast fuzzy string matching
- `fuzzywuzzy` — Fuzzy matching utilities

### **Google Drive Integration**
- `google-api-python-client` — Google Drive API
- `google-auth` — OAuth authentication
- `google-auth-oauthlib` — OAuth flow

### **Statistical Modeling**
- `pymc` — Bayesian statistical modeling
- `arviz` — Bayesian model diagnostics

### **Utilities**
- `pyyaml` — YAML config parsing
- `openpyxl` — Excel file support

---

## 💡 Tips & Best Practices

### **Performance**
- Geocoding results are cached in `data/cache/` — don't delete unless you need to refresh coordinates
- Use `run_data_pipeline.sh` instead of running scripts individually for consistency
- The pipeline only geocodes new cities/properties, reusing cached results

### **Data Privacy**
- Never commit files in `data/` or `secrets/` directories
- All confidential data stays local or in Google Drive
- OAuth tokens are personal — don't share `secrets/token.json`

### **Troubleshooting**
- If geocoding fails: check internet connection and try again (cached results are preserved)
- If OAuth expires: delete `secrets/token.json` and rerun `scripts/01_auth.py`
- If pipeline errors: ensure you've run `pip install -r requirements.txt`

### **Working with Maps**
- Open `.html` map files directly in a web browser
- For best performance, use Chrome or Firefox
- Interactive maps work offline once generated

---

## 🎓 Project Context

This work is part of the **BU Spark! Data Science for Social Good** program, in partnership with the **Citizens' Housing and Planning Association (CHAPA)**.

**Team:** Fall 2025 Team B
**Partner:** CHAPA
**Focus:** Affordable housing application patterns and demographic analysis across Massachusetts

---
