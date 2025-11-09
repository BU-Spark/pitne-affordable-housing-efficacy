# Income and Demographics vs Applicants Analysis

This folder contains the exploratory visualizations developed during the **Proof of Concept (PoC)** phase of the *Affordable Housing (Chapa)* project.  
These visuals were created to investigate the key relationships outlined in our project’s Base Question 3 —  
**“Does the price of an affordable home affect applicant quantity and demographics, controlling for income limits?”**

The following charts provide initial insights into property prices, demographic representation, applicant distribution, and income relationships using the cleaned datasets accessed via Google Drive OAuth (`01_auth.py`).  
Each visualization contributes to building a foundational understanding of patterns in affordable housing demand and accessibility.

---

## 🏠 1. Distribution of Affordable Home Prices  
**File:** `Applicant_by_Affordable_Prices.png`  

This histogram shows how affordable home prices are distributed across available properties.  
Most homes are clustered between **$200,000 and $250,000**, forming the central affordability range for the dataset.  
The smooth density curve indicates that listings drop off gradually beyond $300,000, suggesting that relatively few properties exceed this price threshold.  

**Key Insight:**  
- The concentration of listings around the $200K–$250K mark suggests that this is the most active and attainable price range for affordable housing programs.  
- Higher-priced properties may face fewer applications due to income-based eligibility constraints.

---

## 👥 2. Applicant Distribution by Race / Ethnicity  
**File:** `Applicant_Distribution_by_Race.png`  

This donut chart visualizes the racial and ethnic composition of applicants.  
The largest applicant group identifies as **White (45.8%)**, followed by **Black or African American (10.6%)** and **Asian (9.4%)**.  
Smaller proportions include Hispanic or Latino (7.0%), Asian/Pacific Islander (2.5%), and applicants who chose not to disclose race (2.9%).  

**Key Insight:**  
- The data reveals noticeable demographic disparities — White applicants are significantly overrepresented compared to other groups.  
- These disparities may highlight barriers in outreach, awareness, or access to affordable housing programs among minority communities.

---

## 🧾 3. Distribution of Applicant Counts per Property  
**File:** `DistributionOf_ApplicantCount_perProperty.png`  

This histogram illustrates how many applicants applied per property.  
The distribution is heavily right-skewed — most properties received **fewer than 20 applications**, with only a few receiving over 60–80 applicants.  

**Key Insight:**  
- The uneven applicant distribution suggests that certain properties are more visible or desirable, while others attract limited attention.  
- This may be influenced by factors such as **location, amenities, or accessibility**.  
- Understanding these variations can help identify properties that require better marketing or community outreach.

---

## 💰 4. Relationship Between Home Price and Household Income  
**File:** `RelationOf_HomePrice_&_HouseholdIncome.png`  

This scatter plot examines the relationship between property price and household income among applicants.  
While one might expect higher-priced homes to attract higher-income applicants, the data shows **no clear linear correlation** — applicant income levels are spread widely across all property price ranges.  

**Key Insight:**  
- The lack of a strong relationship suggests that **income limits and program eligibility** likely play a stronger role in determining applicant participation than property price alone.  
- Other contextual factors, such as family size, location preferences, or availability of subsidies, may influence applicant behavior.

---

## 📍 5. Top 15 Cities by Applicant Count  
**File:** `Applicant_by_topCity.png`  

This horizontal bar chart displays the top 15 cities ranked by applicant count.  
The cities with the highest number of applicants are **Worcester, Lowell, and Boston**, followed by Quincy, Taunton, and Andover.  

**Key Insight:**  
- Urban areas like **Boston, Lowell, and Worcester** show the strongest demand for affordable housing, likely due to better job opportunities, public transit access, and educational institutions.  
- Smaller cities with fewer applications may reflect limited property availability or lower public awareness of affordable housing programs.

---

## 🧩 Summary of Findings  

Together, these visualizations provide a coherent early picture of housing affordability dynamics in Massachusetts.  
- **Price distribution** confirms that most listings cluster around the lower to mid-price range ($200K–$250K).  
- **Applicant demographics** reveal racial imbalances in who applies.  
- **Application counts** highlight uneven property interest, with a few listings drawing most of the demand.  
- **Income vs. price analysis** indicates that applicant participation isn’t driven purely by affordability, suggesting other socioeconomic factors.  
- **City-level distribution** points to urban concentration of applications.  

These analyses form the analytical foundation for the next phase, where statistical modeling and predictive analysis will explore these relationships in greater depth.


