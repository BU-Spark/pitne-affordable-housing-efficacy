# Dataset Documentation Questions

## Project Information

### Basic Information
- **What is the project name?**
  CHAPA Affordable Housing Project (Fall 2025, Team B)

- **What is the link to your project's GitHub repository?**
  https://github.com/BU-Spark/ds-chapa-affordable-housing (main repository, project folder: `fa25-team-b/`)

- **What is the link to your project's Google Drive folder?**
  - DS701 subfolder: https://drive.google.com/drive/u/0/folders/16bMXvqP5edlBwRIa4qjO7yVY_K3bDdMD
  - Data folder ID stored in `DATASET_FOLDER_ID` file. Contains confidential CHAPA application data (not publicly accessible).

- **In your own words, what is this project about? What is the goal of this project?**
  This project provides demographic and geographic analysis of applicants to CHAPA's affordable housing properties across Massachusetts. Goals include identifying applicant movement patterns, understanding portfolio biases, analyzing age-restricted housing effects, and examining how demographic factors (race/ethnicity, age, income, assets) influence application patterns. Findings inform CHAPA's policy decisions and outreach strategies to increase housing equity and access.

- **Who is the client for the project?**
  Citizens' Housing and Planning Association (CHAPA) - non-profit focused on affordable housing in Massachusetts

- **Who are the client contacts for the project?**
  David Gasser

- **What class was this project part of?**
  DS701 Tools for Data Science, Fall 2025 semester

### Dataset Overview
- **What data sets did you use in your project? Please provide a link to the data sets.**

  Primary Application Datasets (confidential, stored in private Google Drive):
  1. CHAPA Chapter 40B Application Data (October 2023 to May 2025)
  2. CHAPA Chapter 40B Application Data (June 2021 to September 2023)

  Resale/Property Value Datasets (multiple versions, June 2021 to September 2025):
  3. Resale Transaction Info (multiple versions)
  4. Resale Values (various time periods)

  External Reference Data:
  5. HUD MTSP Income Limit Data (FY 2025): https://www.huduser.gov/portal/datasets/mtsp/mtsp25/MTSP-Data-FY25.xlsx
  6. Massachusetts Cities/Towns Geographic Data - Nominatim (OpenStreetMap)
  7. Massachusetts Town Boundaries (GeoJSON) - cached locally

- **What keywords or tags would you attach to the dataset?**
  affordable housing, Massachusetts, CHAPA, housing applications, demographics, race/ethnicity, income, household assets, age-restricted housing, geographic analysis, geocoding, applicant patterns, housing accessibility, social equity, urban planning, housing policy, HUD income limits, resale values, geospatial analysis

- **What domain(s) of application does this dataset relate to?**
  Urban Planning and Housing Policy, Social Equity and Housing Justice, Demographic Analysis, Geographic Information Systems (GIS), Public Policy and Government Services, Real Estate and Property Markets, Social Services and Nonprofit Operations

## Dataset Composition

### Motivation
- **For what purpose was the dataset created?**
  Datasets were created to manage CHAPA's lottery and application process for affordable housing opportunities. They track applicant demographics, financial characteristics, and housing preferences. For this project, data is analyzed to understand applicant behavior patterns, identify barriers to equitable access, and inform CHAPA's strategic decisions.

- **Was there a specific task in mind?**
  Three main research questions:
  1. Movement & Distance Analysis: Do applicants apply near their current residence? Are they targeting major cities? Are trends changing?
  2. Geographical Range Analysis: Do applicants apply regardless of location? Which regions have high/low interest? Where do out-of-state applicants focus?
  3. Portfolio Effects: How do demographic factors and property characteristics (price, age restrictions) influence applicant diversity and quantity?

- **Was there a specific gap that needed to be filled?**
  Despite previous analyses, key questions remained about proximity preferences, how portfolio composition shapes the applicant pool, impacts of price and complexity on demographic representation, and whether certain groups face different barriers.

### Instance Description
- **What do the instances that comprise the dataset represent?**
  Each instance represents a single application submitted by an individual to a specific CHAPA property. One person can submit multiple applications, so the unit of observation is the application, not the applicant.

- **Are there multiple types of instances?**
  Yes. Three entity types: (1) Applications (rows) - one person applying to one property, (2) Applicants (unique ID Numbers) who may submit multiple applications, (3) Properties - specific affordable housing developments. Analysis examines relationships between these entities.

- **What is the format of the instances?**
  Tabular data with geospatial and time series components. Structured tables (CSV/Excel source, Parquet output) including latitude/longitude coordinates for applicants and properties, and submission dates (June 2021 to May 2025). Supports spatial analysis and temporal analysis.

### Dataset Size
- **How many instances are there in total?**
  - Total Applications: 1,740
  - Unique Applicants: 1,299
  - Unique Properties: ~200+
  - Time Span: June 15, 2021 to May 13, 2025 (~4 years)

  Distribution: 1,017 applicants with 1 application; 180 with 2; 63 with 3; 26 with 4; 9 with 5; 3 with 6; 1 with 7

- **What is the number of fields?**
  Raw data varies by source file. Processed/cleaned data: 35 columns in `applications_clean.parquet`

### Data Fields
- **What data does each instance consist of?**

  Core: ID Number, Submission Date, Application Property, Source

  Demographics: Age, Race/Ethnicity (normalized), Disability

  Household: HH Size, Dependents, HH Type

  Financial: HH Income, HH Assets, FTHB Class

  Geographic (Applicant): matched_city, match_score, match_type, longitude, latitude, full_location_name

  Race/Ethnicity Normalized: race_norm_final, 8 dummy variables (asian, black_african_american, native_american_alaskan_native, white, white_MENA, hispanic, choose_not_to_answer, unknown), is_mixed_race flag

  Property: Maximum Resale Price, cleaned_address, latitude, longitude, full_location_name

  Economic Reference: applicant_MTSP_Income_Limit (HUD income limit)

- **Is it "raw" data or features?**
  Both. Raw fields (Age, HH Size, Income, Assets, Submission Date, original Race/Ethnicity) and engineered features (geocoded coordinates, matched_city, race_norm_final, dummy variables, resale prices, HUD income limits).

- **Please provide a description of the fields.**
  Key transformations: Current Residence → matched_city via fuzzy matching; Race/Ethnicity → race_norm_final (99 entries to 22 categories) plus dummies; Addresses → coordinates via Nominatim geocoding; HH Size + matched_city → applicant_MTSP_Income_Limit via HUD data merge.

### Missing Information
- **Is there any information missing from individual instances?**
  Yes. Age (some "u/a" entries), Race/Ethnicity (choose not to answer/unknown), Financial data (missing HH Income/Assets for some), Geographic matching (out-of-state applicants), Property data (incomplete resale prices), Dependents (some missing).

- **If so, please explain why this information is missing.**
  Applicant choice (race privacy option), data entry issues, out-of-state applicants outside MA reference data, partial resale data availability, schema differences between older and newer datasets.

- **Does this include intentionally removed information?**
  Yes. Personally identifying information (names, addresses, contact info) is excluded, extreme outliers were filtered during EDA (assets > $600K, age < 18), duplicate columns from cleaning dropped, irrelevant fields excluded.

### Individual Identification
- **Is it possible to identify individuals?**
  Direct identification: No (names, addresses removed).
  Indirect identification: Potentially, though difficult. ID Number is internal only. Specific combinations of demographics could narrow to individuals in small populations, but geographic aggregation to city-level provides some protection. All analyses use aggregation for additional anonymization.

- **If so, please describe how.**
  Rare cases with very specific attribute combinations might allow inference (e.g., 67-year-old Asian with 5 dependents in small town), but requires external knowledge and is not feasible from dataset alone.

  Privacy safeguards: Private Google Drive, aggregated outputs only, individual data never published.

## Collection Process

### Collection Mechanisms
- **What mechanisms or procedures were used to collect the data?**

  Primary Data: Provided by CHAPA from their official application system (Chapter 40B lottery). Excel spreadsheets via private Google Drive.

  Resale Data: From CHAPA property transaction records (Excel/Google Sheets).

  HUD Data: Downloaded from HUD public portal (annual updates, FY 2025 used).

  Geographic Data: Nominatim API for geocoding (cached locally).

  MA Boundaries: Public GeoJSON data (downloaded and cached).

- **How were these mechanisms or procedures validated?**
  Cross-referenced dates across files, validated ID uniqueness, compared application counts across periods, checked demographics against MA population statistics, spot-checked geocoded coordinates, validated fuzzy matching with threshold scores, range-checked numeric fields, verified joins via non-null rates.

### Timeframe
- **Over what timeframe was the data collected?**
  Application data: June 15, 2021 to May 13, 2025 (~4 years) in two batches (historical: June 2021-Sept 2023; recent: Oct 2023-May 2025)
  Resale data: June 2021 to September 2025
  HUD data: FY 2025 limits

- **Does this timeframe match the creation timeframe of the data?**
  Yes. Submission Date field contains actual timestamps. Applications recorded near real-time in CHAPA's system. Data pulled Fall 2025; most recent applications from May 2025; newer applications (June-Dec 2025) not yet included.

## Preprocessing/Cleaning/Labeling

### Overview
- **Was any preprocessing/cleaning/labeling of the data done?**
  Yes, extensive preprocessing performed. Raw data required standardization, categorical normalization, geocoding, and external data integration. Fully automated through pipeline script (`scripts/06_clean_applications_pipeline.py`).

  Pipeline steps: (1) Load & standardize columns, (2) Normalize current residence, (3) Geocode applicant locations, (4) Normalize race/ethnicity, (5) Integrate resale prices, (6) Integrate HUD income limits, (7) Geocode properties & calculate distances, (8) Clean data types, (9) Export as Parquet.

### Specific Cleaning Steps
- **What specific cleaning steps were performed?**

  1. Column Standardization: Mapped variant names to canonical (handled schema differences between datasets)
  2. Current Residence: Lowercase, expand abbreviations, merge subregions, fuzzy match against 351 MA cities (RapidFuzz, 80% threshold)
  3. Geographic Encoding: Geocoded via Nominatim API with local caching
  4. Race/Ethnicity: Unicode normalization, symbol removal, separator standardization, 8 major categories created, dummy variables, mixed-race flagging
  5. Resale Data: Loaded multiple files, standardized property names, joined max resale price
  6. HUD Economic Data: Downloaded FY2025 limits, filtered to MA, melted to long format, matched on HH Size + city
  7. Property Geocoding: Geocoded addresses, calculated Haversine distances, cached coordinates
  8. Data Types: Converted dates to datetime64, numerics (handling "$", commas, "k"), stringified complex objects for Parquet

- **Were any scripts or automated processes used?**
  Yes, fully automated. Main: `scripts/06_clean_applications_pipeline.py`. Individual cleaners (7 modules) in `cleaners/` directory. Config: `config/datasets.yaml`, `config/columns.yaml`. Reference: `assets/city_names_norm_ma.csv`. Execute via `./run_data_pipeline.sh` or `PYTHONPATH=. python scripts/06_clean_applications_pipeline.py`.

- **What was done manually vs. programmatically?**
  Programmatic: All loading, merging, renaming, normalization, geocoding, distance calculations, dummy variables, type conversions, exports.
  Manual (one-time): Creating MA city reference file, designing race normalization rules, identifying resale files, creating config mappings.
  Semi-manual: Quality checks, spot-checking geocoding, reviewing unmatched cities, validating normalization, inspecting edge cases.

### Variable-Specific Cleaning

Current Residence → matched_city:
- Initial: 279 unique raw values, typos, abbreviations, out-of-state entries
- Cleaning: Lowercase, expand abbreviations, fuzzy match (80% threshold), record scores
- Final: Standardized MA city names, match scores, out-of-state = null
- Derived: longitude, latitude, full_location_name

Race/Ethnicity → race_norm_final + dummies:
- Initial: 99 unique entries, inconsistent formatting, symbols
- Cleaning: Unicode normalization, symbol removal, separator standardization, progressive normalization (v1-v6), dummy creation
- Final: 22 standardized categories, clean dummies, mixed-race flag
- Derived: 9 binary indicators

Age:
- Initial: Numeric with "u/a", extreme values
- Cleaning: Convert to numeric (coerce "u/a" → NaN), filter age >= 18 in EDA
- Final: float64 with NaN for missing
- Derived: Age bins in analysis scripts

HH Income, HH Assets:
- Initial: Object with "$", commas, "k" suffixes
- Cleaning: Remove symbols, convert "k" to thousands, parse to float64
- Final: Numeric in dollars, NaN preserved, outliers filtered in EDA
- Derived: None in cleaning

Submission Date:
- Initial: Mixed formats
- Cleaning: Parse to datetime64[ns]
- Final: Standard datetime64[ns]
- Derived: Month, year, application year cycles in EDA

Application Property:
- Initial: Mostly consistent
- Cleaning: Minimal, standardized for resale joins
- Final: String property names (~200+)
- Derived: Resale price, geocoded address/coordinates

HH Size, Dependents:
- Initial: Integer values, some missing
- Cleaning: Convert to numeric, preserve NaN, validate HH Size >= Dependents
- Final: int64 for HH Size, float64 for Dependents
- Derived: applicant_MTSP_Income_Limit

Disability, FTHB Class:
- Initial: String categories
- Cleaning: Minimal standardization
- Final: Categorical strings
- Derived: Binary flags in analysis

### Transformations
- **Were any transformations applied to the data?**

  Yes:
  1. Cleaning Mismatched Values: Fuzzy matching for cities, race normalization (99→22 categories), separator standardization
  2. Missing Values: Numeric coercion to NaN, preserved rather than imputed, "unknown" categories for race, left joins preserve all records
  3. Data Type Conversions: Dates to datetime64[ns], numerics with formatting to float64, Unicode normalization, complex objects to JSON strings
  4. Data Aggregation: Row-level data preserved in pipeline; aggregations in analysis scripts only
  5. Dimensionality Reduction: Race (99→22→8 dummies), geographic (full addresses→city coordinates)
  6. Joining: Merged application datasets, joined resale prices, HUD income limits, geocoding results
  7. Redaction/Anonymization: Removed PII, geographic aggregation to city level, internal ID Number only

### Raw Data Preservation
- **Was the "raw" data saved in addition to the preprocessed data?**
  Yes. Original Excel/CSV files in `data/raw/`, intermediate output in `data/interim/df_cleaning_v1.csv`, final cleaned in `data/processed/applications_clean.parquet`.

- **If so, please provide a link or access point to the "raw" data.**
  Local: `data/raw/` (gitignored), pulled via `scripts/04_pull_all.py`
  Google Drive: Private folder (ID in `DATASET_FOLDER_ID`), OAuth authentication required, restricted access

  Access procedure: (1) Get `client_secret.json`, (2) Save to `secrets/` folder, (3) Run `python scripts/01_auth.py`, (4) Run `python scripts/04_pull_all.py`. Alternatively, set up own OAuth via Google Cloud API.

### Code Availability
- **Is the code that was used to preprocess/clean the data available?**
  Yes, all code in GitHub: https://github.com/BU-Spark/ds-chapa-affordable-housing, folder `fa25-team-b/`

  Cleaning: `scripts/06_clean_applications_pipeline.py` (main), 7 cleaner modules in `cleaners/`, `tools/schema.py`, `tools/google_drive.py`, configs in `config/`

  EDA: `eda/CHAPA_TeamB_EDA.ipynb`, `eda/CHAPA_TeamB_EDA_2nd_version.ipynb`, `eda/Bayesian_Model.ipynb`

  Analysis: `scripts/popularity_graph_generation.py`, `scripts/age_analysis.py`, `scripts/folium_map_generation.py`

  Automation: `run_data_pipeline.sh`

## Uses

### Past Tasks
Demographic Analysis (race/ethnicity, age, household type distributions; age-restricted vs non-age-restricted comparisons), Geographic/Spatial Analysis (mapping, distance calculations, regional concentration, out-of-state patterns), Property Demand Analysis (Pareto analysis, price vs volume, popular vs unpopular comparisons), Financial Analysis (income/asset distributions, HUD limit comparisons, age-based patterns), Portfolio Effects (statistical comparison across 16 traits, predictor identification), Time Series (application trends, seasonality, demographic changes), Interactive Visualization (maps, static charts).

### Potential Future Tasks
Predictive Modeling (property popularity, application volume forecasting), Equity/Disparity Analysis (access disparities, barrier identification), Recommendation Systems (property matching, outreach targeting), Network Analysis (application portfolios, property clustering, substitution patterns), Policy Impact Assessment (price cap effects, age restriction effectiveness), Comparison Studies (benchmarking against other programs/states), Causal Inference (property characteristic effects), Text Analysis (if free-text becomes available), Simulation/Optimization (property placement, lottery design).

### Composition Impact
Factors to consider: Selection bias (only applicants, not eligible non-applicants), Geographic limitations (city-level only, out-of-state missing), Temporal coverage (COVID period, extends to May 2025 only), Self-reported demographics (cannot verify accuracy, bias possible), Portfolio composition effects (reflects current CHAPA portfolio), Data completeness (varying missingness patterns), ID Number limitations (household changes not captured), Normalization trade-offs (some nuance lost), Privacy protections (limit spatial precision and linkage).

### Restricted Tasks
Data should not be used for: Individual identification or targeting, Discriminatory applications, Predictive policing or surveillance, Commercial exploitation, Public sharing of individual records, Purposes misaligned with CHAPA's mission. In general, data must not be used to personally identify applicants or for discriminatory purposes.

## Distribution

### Access Type
Internal (Restricted) Access. Contains confidential applicant information. Access limited to BU Spark! team members, CHAPA staff, future researchers with CHAPA approval. Public sharing limited to aggregated statistics, anonymized visualizations, summary reports, code/methodology (without raw data).

### Access Procedure
Current Team: (1) Get `client_secret.json`, (2) Authenticate via `python scripts/01_auth.py`, (3) Download via `python scripts/04_pull_all.py`, (4) Run pipeline via `./run_data_pipeline.sh`

Future Researchers: (1) Request CHAPA access, (2) Contact BU Spark! for Drive permissions, (3) Follow technical setup in README

Security: Never commit data to GitHub, store on encrypted drives, do not share raw files publicly, delete local copies when done, follow BU security policies.

## Maintenance

### Extension/Augmentation
With CHAPA approval: (1) Add new time periods (update `config/datasets.yaml`), (2) Add external datasets (create new cleaners), (3) Improve cleaning scripts (submit pull requests), (4) Contribute analysis scripts (add to `scripts/`). Fork repository, make changes in feature branch, submit pull request. Data contributions require CHAPA approval.

### Future Updates
Likely updates: New application data (post-May 2025), updated property information (new resales/properties), updated reference data (HUD limits annually), methodology improvements (refined cleaning scripts).

Responsible parties: CHAPA (owns raw data, controls access), BU Spark! Team B (initial development), Future BU Spark! teams (may continue), CHAPA data staff (may take over).

Contact: CHAPA for data access, GitHub issues for technical problems, BU Spark! coordinators for ongoing projects.

## Additional Information

### Scripts and Code
Data Acquisition: `01_auth.py`, `02_list_datasets.py`, `03_pull_dataset.py`, `04_pull_all.py`

Cleaning Pipeline: `06_clean_applications_pipeline.py` (main), 7 cleaner modules in `cleaners/`

Analysis & Visualization: `popularity_graph_generation.py`, `age_analysis.py`, `folium_map_generation.py`

EDA: `CHAPA_TeamB_EDA.ipynb`, `CHAPA_TeamB_EDA_2nd_version.ipynb`, `Bayesian_Model.ipynb`

Utilities: `google_drive.py`, `schema.py`

Automation: `run_data_pipeline.sh`

### Key Findings
1. Property Demand Concentrated: ~20% of properties get ~80% of applications (Pareto). Worcester, Lowell, Boston, Quincy, Andover are top origin cities.

2. Proximity is Strongest Predictor: Popular properties 32% closer (median, p=0.004), 23% closer (mean, p=0.01). Distance matters more than price.

3. Younger Households Drive Demand: Popular properties attract 13% younger applicants (mean age ~40 vs ~46, p=0.003). Peak applications from 30-40 age range.

4. Lower Assets Predict Higher Activity: Popular properties attract 48% lower median household assets (p<0.001) but 10% higher median income (p=0.023). Pattern: stable income, limited savings → urgency.

5. Families with Children Seek Popular Properties: 31% more dependents (trending, p=0.11), larger household sizes (11% higher, trending).

6. Age-Restricted Properties Show Lower Diversity: ~50% White vs more diverse non-age-restricted pool. Seniors: lower income, higher assets. Limited geographic availability.

7. Geographic Concentration: Most applications from Greater Boston/eastern MA. Western MA underrepresented.

8. Price Sensitivity Exists But Not Dominant: Lower prices attract more applications overall, but price difference between popular/unpopular not significant (6% lower, p=0.23).

9. Racial Representation Varies: White and Hispanic largest groups. Composition varies significantly across properties.

Patterns: Temporal (seasonal variation, COVID effects), Demographic (age distribution younger, income/asset ratios vary by age), Geographic (urban→urban, suburban dispersed, out-of-state focus on Boston), Application Behavior (most apply to 1-2 properties, multiple applications correlate with income), Property Type (age-restricted distinct profiles, non-age-restricted more diverse).

### Data Quality
Strengths: Comprehensive coverage (~4 years, 1,740 applications, 1,299 applicants), rich demographics, geocoded locations, multiple data sources integrated, longitudinal potential, fully reproducible pipeline.

Limitations: Selection bias (only applicants), missing data (various fields), self-reported information (potential bias), geographic aggregation (city-level only), limited property characteristics, portfolio composition bias, temporal confounding (COVID, economic changes).

Quality Issues Encountered: Inconsistent formatting (typos, symbols, abbreviations), schema mismatches across datasets, geocoding challenges, missing values, data entry errors, Unicode issues, duplicate handling.

How Addressed: Standardization (reference files, fuzzy matching, multi-stage normalization, config mappings), data type cleaning (regex, Unicode normalization, error handling), geocoding strategy (local caching, match scores, graceful failures), missing value handling (preserve as NaN, document patterns), outlier treatment (filter in EDA, document thresholds), validation checks (cross-validation, spot-checks, consistency tests), documentation (code comments, README files, intermediate outputs).

### Privacy and Ethics
Privacy Concerns: PII could identify individuals via attribute combinations. Sensitive financial data. Protected characteristics under fair housing law.

Ethical Considerations: Representation bias (only applicants), algorithmic fairness risks (perpetuating bias), informed consent (secondary use), equity implications (potential misinterpretation), data access equity (restricted vs transparency).

How Addressed:
Privacy Protections: PII removed, geographic aggregation to city level, access controls (OAuth, Drive permissions, gitignored), data use agreement, aggregated reporting only.

Ethical Safeguards: Equity-focused framing (identify barriers, support underserved), transparency (documented methodology, stated limitations, available code), stakeholder engagement (regular CHAPA communication, advocacy sharing), restricted use guidelines (prohibited uses documented, require CHAPA approval), bias awareness (acknowledged limitations, avoided causal claims, contextualized findings).

Ongoing: Maintain protections in future analyses, require fairness audits for predictive modeling, use aggregated data in presentations, discuss access policy changes with CHAPA.
