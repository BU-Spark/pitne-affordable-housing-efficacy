# 📊 Visuals — CHAPA Affordable Housing (Team B, Fall 2025)

This folder contains all visual outputs generated from the exploratory data analysis (EDA) phase of the CHAPA Affordable Housing project.
Each visualization highlights trends in applicant demographics, income distribution, property demand, and housing accessibility across Massachusetts.

---

## 📁 Folder Structure

### **Portfolio Effects Analysis/**
Comprehensive property popularity and demand analysis including interactive maps, static charts, and detailed trait comparisons.

### **Age Restricted Analysis/**
Analysis focused on senior-restricted (55+/62+) properties and applicant demographics.

### **Income and Demographics vs Applications/**
Socioeconomic and demographic analysis exploring how income, race, and other factors influence applications.

---

## 🏠 Portfolio Effects Analysis

All files in this section are located in `Portfolio Effects Analysis/`

### 1. Applications Pareto Chart
**File:** `applications_pareto.png`
**Description:** Shows cumulative distribution of applications across properties.
**Insight:**
A small number of properties account for most applications, following a clear **Pareto (80/20) pattern** — indicating concentrated demand for a few high-profile developments.

---

### 2. Applications vs. Price (Binned)
**File:** `applications_vs_price_binned.png`
**Description:** Compares the number of applications across property price brackets.
**Insight:**
Applicant demand decreases sharply as property price increases.
Lower-priced units attract the majority of applications, confirming **price sensitivity** among affordable housing applicants.

---

### 3. Top Properties — Bar Chart
**File:** `top_properties_bar.png`
**Description:** Highlights properties with the highest total number of applications.
**Insight:**
The same small group of properties dominates demand, suggesting potential **over-subscription** in select towns and a need for more balanced development.

---

### 4. Top Properties — Stacked Chart
**File:** `top_properties_stacked.png`
**Description:** Stacked bars compare demographic composition (e.g., race/income group) across top properties.
**Insight:**
Demographic diversity varies widely — some properties show strong racial or income clustering, implying uneven applicant outreach or property eligibility requirements.

---

### 5. Enhanced Interactive Applications Map
**File:** `applications_map_enhanced.html`
**Description:** Interactive map showing property locations, total applications, demographic composition, and applicant flow patterns.
**Features:**
- Demographic pie chart markers for each property
- Directional flow lines showing applicant origins (10+ miles)
- Property details including bedrooms, price, age data
- Applicant origin circles
- Price heatmap overlay
- Interactive filters for applications, price, distance, and age
**Insight:**
Most applications originate from **eastern Massachusetts**, especially the Greater Boston area.
This spatial concentration highlights the imbalance between housing demand and available supply across regions.

---

### 6. Comparative Trait Analysis (11 visualizations)

These box plot visualizations compare popular properties (top 10%) against all other properties across key characteristics:

#### **6.1 Maximum Resale Price**
**File:** `trait_comparison_price.png`
**Insight:** Popular properties tend to have slightly lower prices (6% lower on average, though not statistically significant), suggesting affordability is a key driver of demand.

#### **6.2 Median Distance from Applicants**
**File:** `trait_comparison_distance_median.png`
**Insight:** Popular properties are significantly closer to applicants (32% lower median distance, p<0.01), indicating strong preference for proximity to current residence.

#### **6.3 Average Distance from Applicants**
**File:** `trait_comparison_distance_avg.png`
**Insight:** Reinforces the proximity preference, with popular properties showing 23% lower average applicant distance (p<0.01).

#### **6.4 Mean Applicant Age**
**File:** `trait_comparison_age_mean.png`
**Insight:** Popular properties attract significantly younger applicants (13% lower mean age, p<0.01), suggesting younger households are more active in the application process.

#### **6.5 Mean Household Size**
**File:** `trait_comparison_hh_size_mean.png`
**Insight:** Popular properties have slightly larger household sizes (11% higher), though not statistically significant.

#### **6.6 Mean Number of Dependents**
**File:** `trait_comparison_dependents_mean.png`
**Insight:** Popular properties attract applicants with more dependents (31% higher mean), suggesting families with children are seeking these properties.

#### **6.7 Median Household Income**
**File:** `trait_comparison_hh_income_median.png`
**Insight:** Popular properties attract applicants with 10% higher median income (p<0.05), indicating those with stable income are more likely to apply to multiple properties.

#### **6.8 Median Household Assets**
**File:** `trait_comparison_hh_assets_median.png`
**Insight:** Popular properties attract applicants with significantly lower assets (48% lower, p<0.001), suggesting those with fewer savings are more actively seeking affordable housing.

#### **6.9 Mean Household Assets**
**File:** `trait_comparison_hh_assets_mean.png`
**Insight:** Confirms the asset pattern with 40% lower mean assets for popular properties (p<0.001).

#### **6.10 Proportion with Disability**
**File:** `trait_comparison_disability_pct.png`
**Insight:** Slightly lower disability rates among popular property applicants (21% lower), though not statistically significant.

#### **6.11 Proportion First-Time Homebuyers**
**File:** `trait_comparison_fthb_pct.png`
**Insight:** Similar first-time homebuyer rates across all properties (3.5% difference, not significant).

---

### 7. Statistical Analysis Export
**File:** `popular_property_traits_analysis.csv`
**Description:** Comprehensive statistical comparison of 16 traits between popular and all properties.
**Contents:**
- Mean, median, and standard deviation for popular vs. all properties
- T-test statistics and p-values
- Statistical significance flags
- Includes all visualized traits plus distance ranges and geographic coordinates

---

### 8. Property Demand Data Export
**File:** `property_demand_with_geo.csv`
**Description:** Property-level dataset with application counts and geographic coordinates.
**Uses:** Mapping, spatial analysis, demand modeling

---

## 👵 Age-Restricted Applicant Analysis  
**Folder:** `Age Restricted Analysis/`  
These plots focus on senior-restricted (55+/62+) properties, exploring how age, income, and race influence applicant participation.

---

### 1. Age Distribution by Bin
**File:** `age_distribution_by_bin.png`  
**Insight:**  
Most applicants fall in the **30–40** age range, with a noticeable drop-off after 52.  
Few seniors (63+) apply overall, showing limited participation among older households.

---

### 2. Age Distribution by Unique Applicant
**File:** `age_distribution_unique.png`  
**Insight:**  
When duplicates are removed, the pattern remains similar — younger adults dominate the application pool, confirming that the affordable housing program primarily attracts early-career households.

---

### 3. Unique Applicants — Age-Restricted vs Non-Age-Restricted
**File:** `unique_applicants_age_restricted_comparison.png`  
**Insight:**  
Applicants aged **52–63** are the majority in senior-restricted properties, while non-age-restricted properties are dominated by younger adults.  
This validates the age segmentation expected in the dataset.

---

### 4. Applications per Age-Restricted Property
**File:** `applications_per_age_restricted.png`  
**Insight:**  
A few properties such as **Methuen (55+)**, **Merrimac (55+)**, and **Falmouth (62+)** receive most of the senior applications.  
This indicates localized popularity and potential demand bottlenecks.

---

### 5. Age Bin vs Race/Ethnicity (Age-Restricted Applicants)
**File:** `age_bin_vs_race_ethnicity.png`  
**Insight:**  
Age-restricted applicants are predominantly **White**, with smaller shares of **Hispanic/Latino** and other racial groups.  
This reflects potential disparities in outreach or awareness among minority senior populations.

---

### 6. Household Income (Log Scale) by Age Bin
**File:** `income_by_age_bin_boxplot.png`  
**Insight:**  
Median income tends to decline with age, while variance widens among older groups — suggesting seniors often rely on assets rather than steady income.

---

### 7. Race/Ethnicity — Age-Restricted vs Non-Age-Restricted
**File:** `race_ethnicity_comparison.png`  
**Insight:**  
Age-restricted applicants are nearly **50% White**, whereas non-age-restricted applications are more racially diverse.  
This demonstrates demographic imbalance in participation across property types.

---

### 🔎 Summary — Age-Restricted Trends
- Affordable housing participation peaks among **30–40 year olds**, with fewer senior applicants overall.  
- Senior (55+/62+) applicants show **lower household income but higher asset levels**.  
- Racial diversity among senior applicants is lower than among the general applicant pool.  
- A few senior developments attract most applications, suggesting limited geographic availability.

---

## 👨‍👩‍👧 Income and Demographics vs Applications  
**Folder:** `Income and Demographics vs Applications/`

These visuals explore how income levels, race, and other demographic factors influence the number of applications per property.

---

### 1. Income Distribution by Property Type
**File:** `income_distribution.png`  
**Insight:**  
Income distribution skews lower among general applicants but slightly higher among age-restricted applicants — reflecting different eligibility and economic contexts.

---

### 2. Applicant Count vs Median Income
**File:** `applicants_vs_income.png`  
**Insight:**  
Properties located in higher-income regions receive fewer total applications, while lower-income regions exhibit much greater demand.  
This reinforces the **inverse relationship between affordability and demand**.

---

### 3. Race/Ethnicity Composition by Property
**File:** `race_ethnicity_by_property.png`  
**Insight:**  
Certain properties show strong racial concentration, while others are more balanced.  
This pattern may indicate local demographic clustering or uneven distribution of outreach programs.

---

### 4. Applications vs Household Assets
**File:** `applications_vs_assets.png`  
**Insight:**  
Applicants with higher assets tend to apply to a broader range of properties, whereas lower-asset applicants concentrate on a few affordable options.  
This suggests that **asset wealth**, not just income, shapes access and mobility in the application process.

---

## 📈 Overall Summary

### Portfolio Effects Analysis Key Findings:
**Popular properties (top 10% by applications) are characterized by:**
- **Proximity** — 32% closer to applicants on average (highly significant)
- **Younger applicants** — 13% lower mean age (highly significant)
- **Lower applicant assets** — 48% lower median household assets (highly significant)
- **Higher applicant income** — 10% higher median household income (significant)
- **More dependents** — 31% higher mean number of dependents
- **Larger households** — 11% higher mean household size
- **Slightly lower price** — 6% lower resale price (not significant)

**Statistical Significance:**
- Distance and proximity are the strongest predictors of property popularity
- Younger households with stable income but lower savings drive demand
- Families with children show strong preference for popular properties
- Price alone is not a significant differentiator

### Age-Restricted Analysis Summary:
- Affordable housing participation peaks among **30–40 year olds**, with fewer senior applicants overall.
- Senior (55+/62+) applicants show **lower household income but higher asset levels**.
- Racial diversity among senior applicants is lower than among the general applicant pool.
- A few senior developments attract most applications, suggesting limited geographic availability.

### Overall Trends:
- **Demand** is concentrated in a small number of properties and regions (primarily eastern MA).
- **Age and income** remain key determinants of housing application activity.
- **Senior (age-restricted)** applicants show lower diversity and smaller total participation.
- **Income-to-asset patterns** highlight structural differences between younger and older applicant groups.
- **Proximity to current residence** is the strongest predictor of property popularity.

---

