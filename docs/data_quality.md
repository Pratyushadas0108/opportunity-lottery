# Data Quality & Outlier Audit Report

**Project**: The Opportunity Lottery  
**Dataset**: `clean_data/state_master.csv`  
**Spatial Coverage**: 36 Indian States and Union Territories  
**Total Records**: 36  
**Total Variables**: 40  
**Audit Date**: 2026-11-13  

---

## 1. Completeness & Missing Value Analysis
- **Total Missing Values**: **0** (100% complete matrix).
- Every indicator across all four official sources (UDISE+ 2024–25, AISHE 2023–24, PLFS 2025, Census 2011) is populated for all 28 States and 8 Union Territories.

### Spatial Harmonization Fixes Logged
1. **Dadra and Nagar Haveli and Daman and Diu**:
   - Reconciled into a single entity across all sources. In Census 2011, population-weighted aggregation was applied to pre-merger Census district records.
2. **Telangana & Andhra Pradesh**:
   - Sourced directly from post-bifurcation official survey tables in UDISE+, AISHE, and PLFS. For Census 2011 demographic baselines, official 2011 Census district reconciliations (10 Telangana districts vs. 13 Andhra Pradesh districts) were applied.
3. **Jammu & Kashmir & Ladakh**:
   - Both entities are reported independently in modern UDISE+, AISHE, and PLFS releases. For Census 2011, Leh and Kargil districts were separated to establish Ladakh's demographic baseline.

---

## 2. Statistical Distribution & Outlier Identification
Outliers were identified using the standard Tukey Interquartile Range method ($\text{Q1} - 1.5 \times \text{IQR}$ or $\text{Q3} + 1.5 \times \text{IQR}$):

| Sub-Index / Dimension | Indicator | Min | Max | Mean | Median | Outlier States & Values | Methodological Reason & Policy Context |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **School Quality** | Secondary PTR | 5.0 | 30.0 | 12.8 | 10.5 | **Jharkhand** (30.0) | High teacher vacancies in secondary schools. |
| **School Quality** | Transition Rate (Upper Prim → Sec) | 65.0% | 99.6% | 90.0% | 91.8% | **Meghalaya** (65.0%), **Bihar** (66.7%) | Severe retention drop-off between middle and high school. |
| **School Quality** | % Functional Electricity | 28.1% | 100% | 90.2% | 96.0% | **Meghalaya** (28.1%), **Arunachal Pradesh** (62.3%), **Manipur** (63.3%) | Hilly/remote terrain and historical grid infrastructure deficits in Northeast states. |
| **School Quality** | % Functional Girls' Toilets | 68.7% | 100% | 92.5% | 96.8% | **Meghalaya** (68.7%), **Arunachal Pradesh** (73.7%) | Infrastructure lags in remote hill-district schools. |
| **Higher Education** | Gross Enrolment Ratio (GER) | 7.09% | 72.31% | 31.89% | 30.12% | **Puducherry** (72.31%) | Small UT serving as a regional higher-education medical/engineering hub. |
| **Higher Education** | Higher Ed PTR | 8.8 | 61.3 | 22.5 | 21.1 | **Bihar** (61.3), **Jharkhand** (53.8) | Overburdened state university colleges with severe faculty shortages. |
| **Higher Education** | College Density (per lakh) | 8.1 | 68.8 | 31.8 | 31.1 | *None* | Steady variance across states (Karnataka & Kerala highest, Bihar lowest). |
| **Jobs & Economy** | Youth Unemployment (15–29) | 2.5% | 31.2% | 13.7% | 13.3% | **Andaman & Nicobar** (31.2%) | Island UT economy with high educated aspiration but constrained formal private sector. |
| **Jobs & Economy** | Female LFPR (15+) | 13.1% | 66.7% | 43.8% | 44.3% | **Delhi** (13.1%) | *The Urban Paradox*: Despite high literacy, metropolitan Delhi exhibits the lowest female labor force participation. |
| **Jobs & Economy** | Regular Wage/Salaried Share | 12.0% | 74.3% | 30.3% | 26.3% | **D&NH and D&D** (74.3%) | Heavy industrial manufacturing hub attracting formal factory employment. |
| **Gender Equality** | Female Youth Unemployment | 2.0% | 41.4% | 16.9% | 15.9% | **Andaman & Nicobar** (41.4%), **Lakshadweep** (40.4%) | Disproportionate friction for young educated women entering island labor markets. |
| **Gender Equality** | Higher Ed GPI | 0.96 | 2.21 | 1.22 | 1.12 | **Lakshadweep** (2.21), **Ladakh** (2.17), **D&NH and D&D** (2.08) | More women than men enrolled in higher education in these UTs (often driven by male youth out-migration for work). |

---

## 3. Exclusion / Weighting Recommendation
- **No States or UTs are excluded**: All 36 entities are retained in the master dataset to provide full geographic coverage of the Republic of India.
- **Handling Small UTs in Analysis**: In subsequent clustering and correlation analysis, small UTs (e.g. Lakshadweep, Ladakh, Puducherry) will be evaluated alongside states, but flagged when institutional scale or small sample size produces high variance.
