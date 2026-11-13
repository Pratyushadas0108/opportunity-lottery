# Empirical Findings Table: The Opportunity Lottery

This document presents verified empirical findings answering the **Seven Core Business Questions**. 
*Note: In accordance with project governance rules, this document provides analytical data and numbers only. Plain-language insights and policy recommendations are authored by the student analyst.*

---

## Reference Periods for Datasets Used Throughout This Report
- **School Indicators (Transition, Retention, Infrastructure)**: **UDISE+ Academic Year 2024–25** (Department of School Education & Literacy, MoE).
- **Higher Education Indicators (GER, GPI, College Density, PTR)**: **AISHE Academic Year 2023–24** (Department of Higher Education, MoE).
- **Labor, Employment & Adult Literacy Indicators (LFPR, Unemployment, Regular Wage)**: **PLFS Calendar Year 2025** (January–December 2025 Survey Period; NSSO, MoSPI).
- **Demographic Baselines (Total Population, Urbanization %)**: **Census of India 2011** (Office of the Registrar General & Census Commissioner, India).

---

## Business Question 1: Overall State Rankings & Groupings

### How do Indian states rank on overall student opportunity, and who sits in the top and bottom groups?

Because Union Territories (UTs) are small and heavily urbanized, rankings are reported across both frameworks:
1. **All 36 States and UTs**
2. **28 States Only** (excluding UTs)

### A. All 36 States & Union Territories Ranking

| Group | States / UTs | Score Range | Key Characteristic |
| :--- | :--- | :---: | :--- |
| **Top 5 Entities** | 1. **Chandigarh** (`70.05`)<br>2. **Puducherry** (`68.81`)<br>3. **D&NH and D&D** (`67.95`)<br>4. **Sikkim** (`67.36`)<br>5. **Tamil Nadu** (`64.92`) | **64.92 – 70.05** | High public school electrification (>90%, UDISE+ AY 2024–25), secondary transition above 90% (UDISE+ AY 2024–25), and high college density (AISHE AY 2023–24). |
| **Bottom 5 Entities** | 32. **Manipur** (`45.70`)<br>33. **Jammu & Kashmir** (`45.58`)<br>34. **Meghalaya** (`43.97`)<br>35. **Arunachal Pradesh** (`41.74`)<br>36. **Bihar** (`35.52`) | **35.52 – 45.70** | Structural bottlenecks: lower school transition (Bihar: 66.7%), higher college student-faculty ratio (Bihar higher-ed PTR: 61.3), or low school electrification (Meghalaya: 28.1%). |

- **Distribution Statistics (36 Entities)**: Mean = `54.49`, Median = `54.80`, Standard Deviation = `7.83`.
- **Top 5 vs. Bottom 5 Divide**: The Top 5 average (`67.82`) is **1.60x higher** than the Bottom 5 average (`42.50`), representing an absolute gap of `25.32` index points.

### B. 28 States Only (Excluding Union Territories)

| State Rank (of 28) | Overall Rank (of 36) | State Name | Opportunity Index | Context |
| :---: | :---: | :--- | :---: | :--- |
| **1** | 4 | **Sikkim** | **67.36** | #1 among all 28 states (Himalayan state, pop ~6.1 lakh). |
| **2** | 5 | **Tamil Nadu** | **64.92** | **#1 among all major states** (population > 10M). |
| **3** | 6 | **Kerala** | **63.94** | High schooling (91.7) & college access (59.0). |
| **4** | 7 | **Himachal Pradesh** | **63.57** | High transition rates and rural electrification. |
| **5** | 8 | **Karnataka** | **59.86** | Balanced higher ed and technology employment. |
| **6** | 9 | **Goa** | **59.04** | High secondary retention. |
| **7** | 10 | **Gujarat** | **58.04** | #1 in employment dynamism (79.95). |
| **8** | 11 | **Uttarakhand** | **57.83** | High school retention and female literacy. |
| **9** | 12 | **Haryana** | **57.59** | High industrial wage share, but low female LFPR. |
| **10** | 14 | **Maharashtra** | **57.38** | High college density and urbanization. |
| ... | ... | ... | ... | ... |
| **24** | 30 | **Jharkhand** | **46.35** | High college PTR (53.8) and faculty shortage. |
| **25** | 32 | **Manipur** | **45.70** | Secondary retention disruptions. |
| **26** | 34 | **Meghalaya** | **43.97** | Lowest school electrification (28.1%). |
| **27** | 35 | **Arunachal Pradesh** | **41.74** | Secondary transition bottlenecks. |
| **28** | 36 | **Bihar** | **35.52** | Lowest overall opportunity score in India. |

---

## Business Question 2: Pipeline Continuity & Transition Bottlenecks

### Do states with higher school indicators also have higher college access and youth job outcomes?

| Pipeline Link | Pearson ($r$) | Spearman ($\rho$) | Empirical Observation (N = 36) |
| :--- | :---: | :---: | :--- |
| **School Quality (UDISE+ AY 2024–25) $\leftrightarrow$ Higher-Ed Access (AISHE AY 2023–24)** | **$+0.512$** | **$+0.532$** | **Moderate-to-Strong Positive Association**: States with higher school facilities, low secondary dropouts, and high transition rates systematically show higher college enrolment. |
| **Higher-Ed Access (AISHE AY 2023–24) $\leftrightarrow$ Youth Jobs & Economy (PLFS CY 2025)** | **$+0.058$** | **$+0.055$** | **No Clear Linear Association**: In this cross-sectional dataset of 36 points, tertiary access does not linearly correlate with immediate youth employment dynamism ($r = +0.058$). Higher-Ed GER has a weak positive correlation with youth unemployment ($r = +0.12$). *(Untested Hypothesis: Educated youth may experience longer search durations/queueing for formal jobs rather than accepting informal work; cross-sectional aggregate data cannot track individual search duration or interstate migration).* |
| **School Quality (UDISE+ AY 2024–25) $\leftrightarrow$ Youth Jobs & Economy (PLFS CY 2025)** | **$+0.058$** | **$+0.055$** | **No Clear Linear Association**: Foundational school facilities do not directly predict immediate state-level youth employment rates. |
| **Higher-Ed Access (AISHE AY 2023–24) $\leftrightarrow$ Gender Equality (Composite)** | **$+0.244$** | **$+0.224$** | **Weak Positive Association**: College availability moderately coincides with female parity in higher education and adult literacy. |

---

## Business Question 3: The Gender Divide Across the Progression Pipeline

### Where does the gender gap widen or narrow across education and the labor market?

*Note: To prevent confusion between population-weighted national statistics and state-level averages, both figures are reported side-by-side. All gaps between percentages are reported in **percentage points**.*

| Educational & Economic Stage | Official All-India National Figure (Source Report) | Unweighted State Average (Mean of 36 States/UTs) | Gender Gap (Male − Female) | Trend / Observation |
| :--- | :---: | :---: | :---: | :--- |
| **1. Adult Literacy (Age 7+)**<br>*(PLFS CY 2025, Table 7)* | Male: **87.5%**<br>Female: **74.9%** | Male: **90.5%**<br>Female: **80.5%** | **$+12.6$ percentage points** (Official)<br>**$+10.0$ percentage points** (Unweighted) | Male advantage in foundational adult literacy. |
| **2. Secondary Retention (Class 9–10)**<br>*(UDISE+ AY 2024–25, Table 6.13)* | Boys: **86.7%** (Drop: 13.3%)<br>Girls: **90.4%** (Drop: 9.6%) | Boys: **87.3%** (Drop: 12.7%)<br>Girls: **90.8%** (Drop: 9.2%) | **$-3.7$ percentage points** (Official)<br>**$-3.5$ percentage points** (Unweighted) | **Female Advantage**: Girls show a 3.5 to 3.7 percentage point higher retention rate than boys. |
| **3. Higher-Ed Enrolment (GER 18–23)**<br>*(AISHE AY 2023–24, Table 19)* | Male: **28.9%**<br>Female: **31.2%**<br>Official GPI: **1.08** | Male: **29.8%**<br>Female: **34.3%**<br>Mean State GPI: **1.22** | **$-2.3$ percentage points** (Official)<br>**$-4.5$ percentage points** (Unweighted) | **Female Advantage**: Female college enrolment exceeds male enrolment. *(Mathematical Note on GPI below)*. |
| **4. Workforce Entry (LFPR 15+ years)**<br>*(PLFS CY 2025, Table 16.0)* | Male: **79.1%**<br>Female: **40.0%** | Male: **77.2%**<br>Female: **43.8%** | **$+39.1$ percentage points** (Official)<br>**$+33.4$ percentage points** (Unweighted) | **Sharp Reversal**: A 33.4 to 39.1 percentage point gap appears at workforce entry. |

#### Mathematical Note on Gender Parity Index (GPI) Difference:
- **Ratio of Unweighted Averages**: $\frac{34.31\% \text{ (Female)}}{29.83\% \text{ (Male)}} = \mathbf{1.15}$.
- **Unweighted Average of State-level GPIs**: $\frac{1}{36}\sum \text{GPI}_i = \mathbf{1.22}$.
- **Official All-India National GPI (AISHE AY 2023–24 Table 19)**: $\frac{31.24\%}{28.91\%} = \mathbf{1.08}$.
- *Why they differ*: In mathematics (Jensen's inequality), the average of ratios $\frac{1}{N}\sum \frac{Y_i}{X_i}$ does not equal the ratio of averages $\frac{\sum Y_i}{\sum X_i}$. In several smaller states and UTs (e.g. Chandigarh GPI = 1.63, Kerala GPI = 1.52, Himachal Pradesh GPI = 1.48), female enrolment is substantially higher than male enrolment, which pulls up the simple arithmetic average of state GPIs to 1.22.

---

## Business Question 4: Outlier Analysis

### Which states diverge from national baseline patterns?

1. **Kerala (High Education, Youth Employment Search Friction)**:
   - School Quality Sub-Index: `91.66` (Rank #2 of 36).
   - Higher-Ed Access Sub-Index: `58.96` (Rank #6 of 36; GER: 41.3%, AISHE AY 2023–24).
   - Youth Jobs Sub-Index: `49.09` (Rank #27 of 36).
   - Youth Unemployment (15–29 years, PLFS CY 2025): `20.8%` (Female youth unemployment: `22.8%`).
   - *(Untested Hypothesis: High educational attainment may raise reservation wages, leading educated youth to search longer for formal jobs rather than accepting informal work).*
2. **Delhi (High Urbanization & Literacy, Low Female Workforce Participation)**:
   - Urbanization: `97.5%` (Census 2011).
   - Female Literacy: `84.4%` (PLFS CY 2025).
   - Female LFPR (15+ years, PLFS CY 2025): **`13.1%` (Lowest across all 36 States & UTs)**.
   - *State Comparison*: Among the 28 full states, Haryana (`23.8%`) and Bihar (`24.7%`) have the lowest female LFPR.
3. **Meghalaya (Gender Parity Strength, School Physical Infrastructure Deficit)**:
   - Gender Equality Sub-Index: `64.82` (Rank #3 of 36; Female LFPR: `64.3%`, PLFS CY 2025).
   - School Quality Sub-Index: **`15.74` (Rank #36 of 36)**.
   - School Electrification: `28.1%` (UDISE+ AY 2024–25, lowest in India; Upper primary to secondary transition: `65.0%`).
4. **Gujarat (Employment Dynamism, Lower Higher-Ed GER)**:
   - Youth Jobs Sub-Index: **`79.95` (Rank #1 among major states)**.
   - Youth Unemployment Rate (15–29 years, PLFS CY 2025): `2.5%` (Lowest in India).
   - Higher-Ed GER (AISHE AY 2023–24): `26.5%` (Sub-index score: `40.02`, Rank #21 of 36).
5. **Bihar (Institutional Capacity Constraints Across Pipeline)**:
   - Opportunity Index: `35.52` (Rank #36 of 36).
   - Higher-Ed Student-Teacher Ratio (AISHE AY 2023–24): **`61.3` students per faculty** (National average: 22.5).
   - College Density (AISHE AY 2023–24): **`8.07` colleges per lakh population** (National average: 31.8).
   - Gender Equality Sub-Index: `26.26` (Rank #36 of 36; Female LFPR: `24.7%`, PLFS CY 2025).

---

## Business Question 5: Structural Profiles (K-Means Clustering)

### Can states be grouped into empirical profiles, and what are the cluster averages?

*Model Selection: $k=4$ clusters across the 4 normalized sub-indices ($X \in \mathbb{R}^{36 \times 4}$). Inertia dropped from 101.91 at $k=2$ to 61.33 at $k=4$; Silhouette Score = 0.271.*
*Naming Rationale: Profiles are named descriptively after their sub-index balance, rather than as ordinal severity tiers, because multidimensional trade-offs exist (e.g. Cluster 4 has a higher school score than Cluster 3, while Cluster 1 has a lower college score than Cluster 2).*

### Exact Cluster Sub-Index Averages

| Profile / Cluster | Entity Count | Mean School | Mean Higher Ed | Mean Jobs | Mean Gender | Mean Composite Index | Structural Profile Description |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Cluster 1: Employment-Led Dynamism** | 4 | **69.56** | **40.03** | **78.65** | **61.98** | **62.55** | High jobs dynamism and regular wage shares; moderate college enrolment. |
| **Cluster 2: Educational Infrastructure Hubs** | 15 | **83.31** | **57.48** | **52.42** | **47.47** | **60.17** | Highest school infrastructure and college access; moderate jobs scores due to youth unemployment search time. |
| **Cluster 3: Gender-Strong / School Infrastructure Lags** | 9 | **50.64** | **40.42** | **45.68** | **55.16** | **47.98** | Primarily northeastern and hill states; strong gender parity but lowest public school infrastructure scores. |
| **Cluster 4: Schooling-Active / Tertiary & Gender Constrained** | 8 | **62.02** | **36.33** | **50.82** | **39.36** | **47.13** | Moderate school scores, but lowest higher-education capacity (high PTR, low density) and lowest gender equity. |

### State Membership per Cluster
- **Cluster 1 (4)**: Dadra and Nagar Haveli and Daman and Diu, Sikkim, Gujarat, Chhattisgarh.
- **Cluster 2 (15)**: Chandigarh, Puducherry, Tamil Nadu, Kerala, Himachal Pradesh, Karnataka, Goa, Delhi, Uttarakhand, Haryana, Maharashtra, Telangana, Punjab, Andhra Pradesh, Lakshadweep.
- **Cluster 3 (9)**: Nagaland, West Bengal, Mizoram, Assam, Tripura, Ladakh, Manipur, Meghalaya, Arunachal Pradesh.
- **Cluster 4 (8)**: Odisha, Madhya Pradesh, Andaman and Nicobar Islands, Rajasthan, Uttar Pradesh, Jharkhand, Jammu and Kashmir, Bihar.

---

## Business Question 6: Targeted Interventions (Top 5 Candidate States)

### If an intervention could start in only 5 states, which should they be and on what empirical rule?

To eliminate researcher discretion, each program list is computed from a **single explicit column calculation** exported directly to `clean_data/q6_targeted_interventions.csv`:

| Strategic Program | Explicit Calculation Rule | Candidate States Selected (Ranked by Need) | Exact Metric Value | Source & Reference Period |
| :--- | :--- | :--- | :---: | :--- |
| **Program A: Public School Infrastructure Upgrades** | **5 lowest values of `subindex_school`** | 1. **Meghalaya**<br>2. **Arunachal Pradesh**<br>3. **Bihar**<br>4. **Manipur**<br>5. **Mizoram** | `15.74`<br>`38.70`<br>`48.27`<br>`50.18`<br>`50.84` | UDISE+ AY 2024–25 (Meghalaya school electrification is 28.1%; Bihar secondary dropout exceeds 15%). |
| **Program B: College Capacity & Faculty Expansion** | **5 lowest values of `subindex_higher_ed`** | 1. **Bihar**<br>2. **Jharkhand**<br>3. **D&NH and D&D**<br>4. **Ladakh**<br>5. **Andaman & Nicobar** | `28.26`<br>`29.21`<br>`31.58`<br>`32.89`<br>`33.78` | AISHE AY 2023–24 (Severe faculty shortages: Bihar college PTR is 61.3, Jharkhand is 53.8; Bihar has only 8.07 colleges per lakh population). |
| **Program C: Female Workforce Transition Support** | **5 lowest values of `female_lfpr_15_plus`** | 1. **Delhi**<br>2. **Lakshadweep**<br>3. **Haryana**<br>4. **Bihar**<br>5. **Goa** | `13.10%`<br>`21.90%`<br>`23.80%`<br>`24.70%`<br>`27.40%` | PLFS CY 2025, Table 16.0 (Lowest female workforce participation across all states and UTs). |

*Reproducibility file: `clean_data/q6_targeted_interventions.csv` generated by `scripts/run_analysis.py`.*

---

## Business Question 7: Sensitivity & Ranking Stability

### How stable is the state ranking if indicator weights change?

| Weighting Model Tested | School Weight | Higher Ed Weight | Jobs Weight | Gender Weight | Spearman Rank Correlation ($\rho$) with Baseline | Average State Rank Shift | Maximum Observed Shift |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Equal Weights)** | **25%** | **25%** | **25%** | **25%** | **$1.000$** | — | — |
| **Scenario 1: Jobs Prioritized** | 20% | 20% | **40%** | 20% | **$+0.901$** | $\pm 1.8$ ranks | Gujarat rises +4 ranks (#10 → #6); D&NH and D&D takes #1. |
| **Scenario 2: School Prioritized** | **40%** | 20% | 20% | 20% | **$+0.938$** | $\pm 1.4$ ranks | Kerala rises +1 rank (#6 → #5); Chandigarh holds #1. |
| **Scenario 3: Gender Prioritized** | 20% | 20% | 20% | **40%** | **$+0.904$** | $\pm 1.7$ ranks | Meghalaya rises +5 ranks (#34 → #29); Rajasthan drops -6 ranks (#28 → #34). |

**Robustness Verdict**: Spearman rank correlation remains **$\ge 0.901$ across all three weighting models**, confirming that the state ranking hierarchy is structurally stable and not driven by arbitrary equal weighting.
