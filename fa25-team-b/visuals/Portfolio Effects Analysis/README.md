# 📊 Portfolio Effects Analysis

This folder contains comprehensive visualizations and statistical analyses examining what factors influence property popularity in the CHAPA affordable housing portfolio.

---

## 🎯 Analysis Overview

This analysis compares the **top 10% most popular properties** (by application volume) against all properties to identify key differentiating characteristics. The analysis includes:

- **4 overview visualizations** showing demand patterns and concentration
- **11 trait comparison visualizations** comparing popular vs. unpopular properties
- **1 interactive map** with demographic overlays and flow analysis
- **2 data exports** for further analysis

---

## 📈 Overview Visualizations

### 1. Applications Pareto Chart
**File:** `applications_pareto.png`

Shows the cumulative distribution of applications across all properties, demonstrating that a small number of properties account for the majority of applications (classic 80/20 pattern).

**Key Insight:** Property demand is highly concentrated, with ~20% of properties receiving ~80% of applications.

---

### 2. Applications vs. Price (Binned)
**File:** `applications_vs_price_binned.png`

Analyzes the relationship between property maximum resale price and application volume across price brackets.

**Key Insight:** Lower-priced properties attract more applications, confirming price sensitivity among applicants.

---

### 3. Top Properties — Bar Chart
**File:** `top_properties_bar.png`

Bar chart ranking the top 15 properties by total application count.

**Key Insight:** Identifies specific high-demand properties for focused analysis.

---

### 4. Top Properties — Stacked Demographics
**File:** `top_properties_stacked.png`

Stacked bar chart showing racial/ethnic demographic composition across the top 15 properties.

**Key Insight:** Demographic diversity varies significantly across popular properties.

---

## 🔍 Trait Comparison Analysis (11 Visualizations)

Each visualization compares popular properties (top 10%) against all other properties using box plots. Statistical significance is indicated when p < 0.05.

### Property Characteristics

#### Maximum Resale Price
**File:** `trait_comparison_price.png`
- **Finding:** Popular properties are 6% cheaper on average
- **Significance:** Not statistically significant (p=0.23)
- **Interpretation:** While popular properties tend to be slightly cheaper, price alone doesn't strongly predict popularity

---

### Distance & Proximity Metrics

#### Median Distance from Applicants
**File:** `trait_comparison_distance_median.png`
- **Finding:** Popular properties are 32% closer to applicants (median distance)
- **Significance:** Highly significant (p=0.004)
- **Interpretation:** **Proximity to current residence is the strongest predictor of popularity**

#### Average Distance from Applicants
**File:** `trait_comparison_distance_avg.png`
- **Finding:** Popular properties are 23% closer to applicants (mean distance)
- **Significance:** Highly significant (p=0.01)
- **Interpretation:** Confirms the strong proximity preference

---

### Applicant Demographics

#### Mean Applicant Age
**File:** `trait_comparison_age_mean.png`
- **Finding:** Popular properties attract applicants who are 13% younger on average
- **Significance:** Highly significant (p=0.003)
- **Interpretation:** Younger households (likely early-career families) are more actively applying

#### Mean Household Size
**File:** `trait_comparison_hh_size_mean.png`
- **Finding:** Popular properties have 11% larger household sizes
- **Significance:** Not significant (p=0.12)
- **Interpretation:** Trend toward larger households but not conclusive

#### Mean Number of Dependents
**File:** `trait_comparison_dependents_mean.png`
- **Finding:** Popular properties attract applicants with 31% more dependents
- **Significance:** Not significant (p=0.11)
- **Interpretation:** Strong trend suggesting families with children prefer popular properties

---

### Financial Characteristics

#### Median Household Income
**File:** `trait_comparison_hh_income_median.png`
- **Finding:** Popular properties attract applicants with 10% higher median income
- **Significance:** Significant (p=0.023)
- **Interpretation:** Applicants with stable income are more likely to apply to multiple properties

#### Median Household Assets
**File:** `trait_comparison_hh_assets_median.png`
- **Finding:** Popular properties attract applicants with 48% lower median assets
- **Significance:** Highly significant (p<0.001)
- **Interpretation:** **Those with lower savings are more urgently seeking affordable housing**

#### Mean Household Assets
**File:** `trait_comparison_hh_assets_mean.png`
- **Finding:** Popular properties attract applicants with 40% lower mean assets
- **Significance:** Highly significant (p<0.001)
- **Interpretation:** Confirms the strong asset pattern

---

### Special Status

#### Proportion with Disability
**File:** `trait_comparison_disability_pct.png`
- **Finding:** 21% lower disability rate among popular property applicants
- **Significance:** Not significant (p=0.56)
- **Interpretation:** No clear pattern for disability status

#### Proportion First-Time Homebuyers
**File:** `trait_comparison_fthb_pct.png`
- **Finding:** 3.5% lower first-time homebuyer rate
- **Significance:** Not significant (p=0.72)
- **Interpretation:** First-time homebuyer status is similar across all properties

---

## 🗺️ Interactive Map

### Enhanced Applications Map
**File:** `applications_map_enhanced.html`

Interactive Folium map with multiple data layers:

**Features:**
- **Property markers:** Pie charts showing demographic composition
- **Flow lines:** Directional arrows showing applicant origins (10+ miles only)
- **Applicant circles:** Origin points sized by application count
- **Price heatmap:** Graduated colors showing property prices
- **Interactive filters:** Filter by applications, price, distance, age

**Usage:** Open in web browser (works offline after generation)

---

## 📊 Data Exports

### Statistical Analysis
**File:** `popular_property_traits_analysis.csv`

Complete statistical comparison across 16 traits:
- Mean, median, standard deviation for popular vs. all properties
- Difference in means and medians
- Percent difference
- T-test statistics and p-values
- Statistical significance flags

**Use Cases:** Further statistical modeling, reporting, presentation

---

### Property Demand Data
**File:** `property_demand_with_geo.csv`

Property-level dataset with:
- Property address and coordinates
- Application counts
- Geographic data (latitude, longitude)
- Property attributes (bedrooms, age restriction where available)

**Use Cases:** Spatial analysis, mapping, demand modeling

---

## 🎯 Key Takeaways

### Statistically Significant Predictors of Property Popularity:

1. **Proximity (Strongest)** — Popular properties are 32% closer to applicants
2. **Applicant Age** — Popular properties attract 13% younger applicants
3. **Applicant Assets** — Popular properties attract applicants with 48% lower assets
4. **Applicant Income** — Popular properties attract applicants with 10% higher income

### Profile of Popular Property Applicants:

- **Younger** (mean age ~40 vs. ~46)
- **Higher income but lower assets** (median income $66K vs. $61K, but assets $33K vs. $63K)
- **Closer to property** (median distance 11 miles vs. 17 miles)
- **More dependents** (0.6 vs. 0.5, trending but not significant)
- **Larger households** (2.1 vs. 1.9 people, trending but not significant)

### Strategic Implications:

1. **Location is critical** — Properties near population centers will naturally attract more applications
2. **Target demographic** — Young families with stable income but limited savings
3. **Urgency factor** — Lower-asset applicants show higher application activity
4. **Price is secondary** — Proximity and applicant demographics matter more than price alone

---

## 📝 Methodology Notes

- **Popular properties** defined as top 10% by application count (20 out of 200 properties)
- **Statistical tests** use Welch's t-test (does not assume equal variances)
- **Significance threshold** set at p < 0.05
- **Box plots** show: quartiles (box), median (line), mean (diamond), whiskers (1.5×IQR)
- **Sample sizes** vary by trait due to missing data; counts shown on each visualization

---

## 🔄 Reproducibility

These visualizations are generated automatically by:

```bash
python scripts/popularity_graph_generation.py --input data/processed/applications_clean.parquet
```

The script:
1. Loads cleaned application data
2. Aggregates applicant traits by property
3. Identifies top 10% most popular properties
4. Performs statistical comparisons
5. Generates all visualizations and exports

---

**Generated:** December 9, 2025
**Team:** CHAPA Affordable Housing Analysis (Fall 2025, Team B)
**Partner:** Citizens' Housing and Planning Association (CHAPA)
