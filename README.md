
<h1 align="center">
  <br>
  <a href="https://www.bu.edu/spark/" target="_blank"><img src="https://www.bu.edu/spark/files/2023/08/logo.png" alt="BUSpark" width="200"></a>
  <br>
  Project README Template <change to project name>
  <br>
</h1>

<h4 align="center">A template for the project readme file. </h4> <change to repo short description>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#project-description">Project Description</a> •
  <a href="#data-locations">Data Locations</a>
</p>

## Key Features
In this section you will be including a list of key features of your code/project.

You should also include a short description of what each part of your code does. (Detailed description in the readme of each directory, if applicable)
* /path/to/directory - function and description
  - Key notes
* /path/to/script - function and description
  - Key notes
* Lorem Ipsum - Dolor Sit Amet
  - Consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
* Duis Aute Irure Dolor
  - Excepteur sint occaecat
* Excepteur Sint Occaecat
  - Curabitur efficitur, nunc non ultricies gravida, felis purus posuere eros, sed faucibus sapien est nec quam. Nulla at nisl nisl.
 
## How To Use

To clone and run this application, you'll need <a href="https://git-scm.com" target="_blank">Git</a>
From your command line:

```bash
# Clone this repository
$ git clone [repo link]

# Further Instructions
...
```

Create a new branch from dev, add changes on the new branch you just created.

You will want to look into <a href="https://git-scm.com/docs/git-branch" target="_blank">git branch</a> and <a href="https://git-scm.com/docs/git-checkout" target="_blank">git checkout</a>

```bash
# Create and Checkout a new branch if it doesn't exist
$ git checkout -b your-branch main
...
```

Open a Pull Request to dev. Add your PM and TPM as reviewers. 

At the end of the semester during project wrap up open a final Pull Request to main from dev branch.
 
## Project Description

In this section, you should include the project description, either from the client or spark.

Please make sure it reflects what you see on the documents (project description) you recieved.

* Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Donec vel nunc at libero ultrices tincidunt. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Mauris ut ligula nec risus posuere ultricies at et ligula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
* Veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Data locations

In this section, you should include the location of all of your datasets for the project (if applicable)

<a href="dataset-documentation">Dataset Documentation</a>

### 🧩 `assets/`
Contains static reference files and lookup tables used to support cleaning and analysis.  
- Example: `city_names_norm_ma.csv` — standardized list of Massachusetts city names used for matching and geographic encoding.  
- These files do not change frequently and are used by scripts in `cleaners/` or `tools/`.

---

### 🧹 `cleaners/`
Houses Python scripts that clean, normalize, and preprocess the raw CHAPA dataset.  
Each script focuses on a specific aspect of data preparation before analysis.  
- **`append_resale_data.py`** → merges resale property data.  
- **`current_residence_name_normalization.py`** → standardizes “current residence” fields.  
- **`geographic_encoding_ma_cities.py`** → adds latitude/longitude for Massachusetts cities.  
- **`HUD_economic_data_import_cleaning.py`** → integrates HUD economic data for contextual variables.  
- **`race_norm_corrections.py`** → normalizes racial/ethnic categories for consistency.  
- **`__init__.py`** → allows the folder to be imported as a Python package.

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
- May contain cleaned `.csv` or `.parquet` files created during preprocessing.  
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
- **`analyze_property_popularityV2.py`** → analyzes property-level application demand.  
Together, these scripts automate the end-to-end data preparation process.

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