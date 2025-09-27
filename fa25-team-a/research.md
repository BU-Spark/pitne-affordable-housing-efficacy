# Initial research

## Problem
### 1. Movement and Distance analysis
*How far an applicant is willing to move from their current home? How does the applicant geographic range compare between different demographic groups?*
* Depending on which organization is responsible, the application can be very different (e.g., requiring extra documentation, longer)
* Out-of-state applicants are allowed. CHAPA observes a limited number of out-of-state applicants, with applicants from New Hampshire occasionally.
* The standard and 55+ applications have very different markets / buyer groups, which CHAPA observes as almost two separate programs. Analysis should be separated.

### 2. CHAPA's limited property pool
*To what extent are the applicant demographics driven by CHAPA’s limited property pool (suburban, age-restricted homes) versus applicant choice?*
* All applicants are put into a lottery system for CHAPA's housing. The lottery system is randomized, but certain people are prioritized for certain homes.
  * For example, people with disabilities are prioritized when the lottery system is picking for accessible houses.
     * People with disabilities are more likely to get picked for housing overall, since they have a smaller population demographic.
* CHAPA is assigned properties to manage, which limits CHAPA's influence in affordable homeownership to monitoring and policy advocacy.
* Applicants are encouraged to apply to multiple properties.
* CHAPA applicants apply from a range of sources.

### 3. Price in Affordable homeownership
*Does the price of the affordable home affect applicant quantity and demographics, controlling for income limits?*
* The housing market across communities can be vastly different. Prices vary region to region.
* Affordable homes at CHAPA are below the 80% AMI threshold.

## Possible solution approaches
### 1. Approach for movement and distance analysis
*How far an applicant is willing to move from their current home?*
* To analyze how far an applicant is willing to move from their current home, we can compare the zip codes of the house applied for and current home address (refer to columns **Application Property** and **Current Residence** in CHAPA Chapter 40B Application Data dataset).
* Using **Applicant ID** as a primary key, conduct separate spatial analysis for standard and 55+ applicants, with PIT-NE Summer team's cleaned age-restricted datasets.
* Distance between the two addresses can be measured by commute time.
  * Commute time could also provide insight into accessibility of a place. E.g.: applicants moving to a place with greater public transit accessibility.
    
*How does the applicant geographic range compare between different demographic groups?*
* Use PIT-NE team's demographic grouping to compare each demographic group's average geographic movement (based on commute time).
* Analyze location demand differences across demographic groups (can refer to PITNE's team CHAPA final report, visualization on page 80).

### 3. Analyzing effects of price on applicant quantity and demographics
*Price of affordable homes impacting applicant quantity*
* We can focus on certain areas that have high demand - which could possibly experience greater changes (or increases) in price across time - to analyze how the number of applications from each demographic changes for those areas.
* Possible model(s): Poisson or negative binomial regression model
  * Feature variable price is used to model count of applications.

*Price of affordable homes impacting demographics*
* Reports from the summer team can provide information to compare towns that receive a high demand of applications from Households of Color vs Non-households of color, and create clusters based on price to analyze for a correlation between the two.
* Similarly, we can compare proportions of different demographics applications (such as different income levels) to towns with highest price and those with lowest price.\
* Possible model(s): Multinomial regression
  * The model would estimate how changes in price affect the probability that an applicant belongs to each demographic group.
## Citations
