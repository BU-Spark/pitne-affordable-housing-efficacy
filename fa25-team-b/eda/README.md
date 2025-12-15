# CHAPA Team B – Exploratory Data Analysis

This repository contains the Exploratory Data Analysis (EDA) for the CHAPA Affordable Housing Project conducted by Team B.

The goal of this analysis is to understand the demographic, financial, and temporal patterns of housing applicants from 2021 to 2025, using CHAPA’s Chapter 40B application and resale datasets.

The EDA provides a foundation for downstream modeling and policy analysis by identifying key patterns, data quality issues, and trends in applicant behavior.

### Data Preparation

Before analysis, all datasets were cleaned and standardized:

- Converted Submission Date to a valid datetime format and handled missing values.
- Removed duplicates and invalid records (e.g., applications with missing or incorrect age values).
- Filtered applicants to include only Age ≥ 18 and Household Assets ≤ $600,000 to eliminate unrealistic or extreme entries.
- Standardized numeric variables (e.g., removed $, commas, and “k” suffixes from HH Income and HH Assets).

These preprocessing steps ensured the consistency and comparability of all downstream visualizations and metrics.

### Application Trends Over Time

- Aggregated monthly submissions into June–May “application years” to align with CHAPA’s reporting cycle.
- Visualized the number of applications per month using bar and line charts, with red dashed lines showing each year’s average submission level.
- Computed the average monthly share (%) of annual submissions across all years to capture seasonality.

### Demographic Distribution (Age)

- Visualized the Age distribution of applicants using histograms, density (KDE) plots, and boxplots.
- Focused on applicants aged 18 to 80 years.

### Financial Characteristics

Household Income and Assets

- Cleaned and standardized HH Income and HH Assets fields for numeric analysis.

### Income and Resale Value Relationship

- Visualized the relationship between **household income** and **maximum resale value**.
- Found that higher household income generally corresponds to slightly higher resale value,  
  but correlation remains **weak to moderate** due to program caps.

### Race and Ethnicity
- Standardized race categories (White, Asian, Hispanic, Black/African American, Native American, MENA, Unknown).
- Compared **Mixed vs Single Race** distributions using stacked horizontal bar charts.
- White and Hispanic groups form the largest proportions of applicants.

## How to Reproduce
Open the notebook in **Google Colab** and make sure upload the datasets which can be download from the github file.
