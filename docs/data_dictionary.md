# Data Dictionary: The Opportunity Lottery

This data dictionary defines every variable, identifier, normalized metric, and composite sub-index across `clean_data/state_master.csv` and `clean_data/opportunity_index.csv`.

---

## 1. Primary Entity Identifiers

| Column Name | Data Type | Description | Source / Standard | Example |
| :--- | :--- | :--- | :--- | :--- |
| `state_code` | String (2 char) | ISO 3166-2:IN two-letter geographic state code | ISO Standard | `TN`, `KL`, `BR` |
| `state_name` | String | Canonical official name of the State or Union Territory | Master State Reference | `Tamil Nadu`, `Bihar` |
| `entity_type` | Categorical | Administrative status (`State` or `Union Territory`) | Ministry of Home Affairs | `State`, `Union Territory` |

---

## 2. Variables in `clean_data/state_master.csv`

### A. School Access & Quality (UDISE+ 2024–25)
*Source: Department of School Education & Literacy, Ministry of Education, Government of India.*

| Column Name | Type | Unit | Definition | Direction | Min / Max |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `ptr_secondary` | Float | Ratio | Pupil-Teacher Ratio at secondary level (Classes IX–X). | Lower is better | 5.0 / 30.0 |
| `dropout_sec_total` | Float | % | Annual average dropout rate for Class IX–X (Total). | Lower is better | 2.0% / 20.0% |
| `dropout_sec_boys` | Float | % | Annual average dropout rate for Class IX–X (Boys). | Lower is better | 2.8% / 23.4% |
| `dropout_sec_girls` | Float | % | Annual average dropout rate for Class IX–X (Girls). | Lower is better | 1.1% / 17.7% |
| `dropout_sec_gender_gap`| Float | % pts | Secondary dropout gap: Girls % − Boys %. | Lower is better | −7.6 / 1.8 |
| `transition_rate_upprim_to_sec`| Float | % | Transition rate from Upper Primary (Class VIII) to Secondary (Class IX). | Higher is better | 65.0% / 99.6% |
| `pct_schools_electricity` | Float | % | Share of all schools with functional electricity connection. | Higher is better | 28.1% / 100.0% |
| `pct_schools_girls_toilet` | Float | % | Share of all schools with functional separate girls' toilets. | Higher is better | 68.7% / 100.0% |
| `pct_schools_computers` | Float | % | Share of all schools with functional computer facilities for pedagogy. | Higher is better | 10.3% / 100.0% |
| `pct_schools_internet` | Float | % | Share of all schools with active internet access. | Higher is better | 16.0% / 100.0% |
| `udise_year` | String | Text | Reporting school year (`2024-25`). | Metadata | `2024-25` |

---

### B. Higher-Education Access (AISHE 2023–24)
*Source: Department of Higher Education, Ministry of Education, Government of India.*

| Column Name | Type | Unit | Definition | Direction | Min / Max |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `ger_higher_ed_total` | Float | % | Gross Enrolment Ratio (GER) in higher education (18–23 age cohort). | Higher is better | 7.09% / 72.31% |
| `ger_higher_ed_male` | Float | % | Male Gross Enrolment Ratio in higher education. | Higher is better | 4.51% / 71.79% |
| `ger_higher_ed_female` | Float | % | Female Gross Enrolment Ratio in higher education. | Higher is better | 9.97% / 72.80% |
| `gpi_higher_ed` | Float | Ratio | Gender Parity Index in tertiary enrolment (Female GER / Male GER). | Higher is better | 0.96 / 2.21 |
| `colleges_per_lakh_pop`| Float | Count | Number of colleges per 100,000 eligible population (18–23 years). | Higher is better | 8.07 / 68.80 |
| `avg_enrolment_per_college` | Float | Count | Average number of students enrolled per college. | Higher is better | 118.4 / 1941.8 |
| `ptr_higher_ed` | Float | Ratio | Pupil-Teacher Ratio across regular-mode colleges and universities. | Lower is better | 8.8 / 61.3 |
| `aishe_year` | String | Text | Academic survey year (`2023-24`). | Metadata | `2023-24` |

---

### C. Jobs & Economy (PLFS Calendar Year 2025)
*Source: National Sample Survey Office (NSSO), MoSPI, Government of India.*

| Column Name | Type | Unit | Definition | Direction | Min / Max |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `youth_unemployment_rate_15_29` | Float | % | Unemployment rate among youth aged 15–29 (Usual Status ps+ss). | Lower is better | 2.5% / 31.2% |
| `youth_female_unemployment_rate`| Float | % | Unemployment rate among female youth aged 15–29. | Lower is better | 2.0% / 41.4% |
| `youth_male_unemployment_rate` | Float | % | Unemployment rate among male youth aged 15–29. | Lower is better | 2.7% / 23.2% |
| `overall_unemployment_rate` | Float | % | Unemployment rate across all ages (Usual Status ps+ss). | Lower is better | 0.9% / 10.0% |
| `youth_lfpr_15_29` | Float | % | Labour Force Participation Rate for youth aged 15–29. | Higher is better | 26.4% / 61.6% |
| `female_lfpr_15_plus` | Float | % | Female Labour Force Participation Rate for persons aged 15+ years. | Higher is better | 13.1% / 66.7% |
| `regular_wage_salaried_share` | Float | % | Share of total workforce in regular salaried/wage employment. | Higher is better | 12.0% / 74.3% |
| `female_literacy_rate_plfs` | Float | % | Female literacy rate for age 7+ (Rural+Urban). | Higher is better | 63.7% / 99.8% |
| `male_literacy_rate_plfs` | Float | % | Male literacy rate for age 7+ (Rural+Urban). | Higher is better | 77.7% / 99.8% |
| `total_literacy_rate_plfs` | Float | % | Total literacy rate for age 7+ (Rural+Urban). | Higher is better | 71.4% / 99.8% |
| `literacy_gender_gap_plfs` | Float | % pts | Literacy gender gap: Male % − Female % (age 7+). | Lower is better | 0.0 / 20.8 |
| `plfs_year` | String | Text | Survey reference year (`2025`). | Metadata | `2025` |

---

### D. Census 2011 Demographic Baselines
*Source: Office of the Registrar General & Census Commissioner, India.*

| Column Name | Type | Unit | Definition |
| :--- | :--- | :---: | :--- |
| `population_2011` | Integer | Count | Total enumerated population in Census 2011 (reconciled boundaries). |
| `urban_population_pct_2011` | Float | % | Percentage of state population residing in urban areas (2011). |
| `literacy_rate_2011` | Float | % | Effective literacy rate (age 7+) in Census 2011. |
| `female_literacy_rate_2011` | Float | % | Female literacy rate (age 7+) in Census 2011. |
| `literacy_gender_gap_2011` | Float | % pts | Literacy gap in 2011: Male % − Female %. |
| `census_year` | String | Text | Census enumeration year (`2011`). |

---

## 3. Variables in `clean_data/opportunity_index.csv`

### A. Normalized Indicators (`norm_*`)
All indicators scaled 0–100 via Min-Max. Inverted indicators flipped via $100 - S$ so that **100 is always the best performance**:
- `norm_ptr_secondary`: Higher score = lower PTR (more teachers per pupil).
- `norm_dropout_sec_total`: Higher score = lower dropout rate.
- `norm_transition_rate_upprim_to_sec`: Higher score = higher retention into secondary.
- `norm_pct_schools_electricity`: Higher score = greater electrification.
- `norm_pct_schools_girls_toilet`: Higher score = greater girls' toilet coverage.
- `norm_pct_schools_computers`: Higher score = greater digital pedagogical infrastructure.
- `norm_ger_higher_ed_total`: Higher score = higher college enrolment.
- `norm_colleges_per_lakh_pop`: Higher score = greater physical college density.
- `norm_avg_enrolment_per_college`: Higher score = greater institutional scale.
- `norm_ptr_higher_ed`: Higher score = lower higher-ed PTR (less overcrowded colleges).
- `norm_youth_unemployment_rate_15_29`: Higher score = lower youth unemployment.
- `norm_overall_unemployment_rate`: Higher score = lower macro unemployment.
- `norm_youth_lfpr_15_29`: Higher score = greater youth economic participation.
- `norm_regular_wage_salaried_share`: Higher score = higher formal/regular employment.
- `norm_gpi_higher_ed`: Higher score = higher female-to-male tertiary participation.
- `norm_female_lfpr_15_plus`: Higher score = higher female economic participation.
- `norm_female_literacy_rate_plfs`: Higher score = higher female literacy.
- `norm_literacy_gender_gap_plfs`: Higher score = narrower gender literacy gap.
- `norm_youth_female_unemployment_rate`: Higher score = lower young female unemployment.
- `norm_dropout_sec_gender_gap`: Higher score = lower dropout penalty for girls.

---

### B. Thematic Sub-Indices & Opportunity Index

| Column Name | Formula / Derivation | Range | Interpretation |
| :--- | :--- | :---: | :--- |
| `subindex_school` | Mean of 6 normalized school indicators | 0–100 | Holistic quality and accessibility of school education. |
| `subindex_higher_ed` | Mean of 4 normalized higher education indicators | 0–100 | Capacity, enrolment, and instructional scale of tertiary education. |
| `subindex_jobs` | Mean of 4 normalized labor market indicators | 0–100 | Labor market dynamism, youth absorption, and job quality. |
| `subindex_gender` | Mean of 6 normalized gender parity indicators | 0–100 | Parity across the pipeline (literacy, school, college, workforce). |
| `opportunity_index` | Equal-weight mean: $0.25 \times (\text{School} + \text{HigherEd} + \text{Jobs} + \text{Gender})$ | 0–100 | **Core composite benchmark of student opportunity**. |
| `rank_baseline` | State rank on `opportunity_index` (1 = Highest, 36 = Lowest) | 1–36 | Primary state ranking. |

---

### C. Sensitivity Stress-Testing Variables

| Column Name | Formula / Weights | Range | Scenario Purpose |
| :--- | :--- | :---: | :--- |
| `index_jobs_focus` | $0.40 \times \text{Jobs} + 0.20 \times (\text{School} + \text{HigherEd} + \text{Gender})$ | 0–100 | Tests priority of skilling/employment funds. |
| `rank_jobs_focus` | State rank on `index_jobs_focus` | 1–36 | Rank under jobs-heavy model. |
| `rank_shift_jobs` | `rank_baseline` − `rank_jobs_focus` | Integer | Positive = state rises; Negative = state drops. |
| `index_school_focus` | $0.40 \times \text{School} + 0.20 \times (\text{HigherEd} + \text{Jobs} + \text{Gender})$ | 0–100 | Tests priority of school infrastructure programs. |
| `rank_school_focus` | State rank on `index_school_focus` | 1–36 | Rank under school-heavy model. |
| `rank_shift_school` | `rank_baseline` − `rank_school_focus` | Integer | Rank shift under school priority. |
| `index_gender_focus` | $0.40 \times \text{Gender} + 0.20 \times (\text{School} + \text{HigherEd} + \text{Jobs})$ | 0–100 | Tests priority of girls' education & empowerment funds. |
| `rank_gender_focus` | State rank on `index_gender_focus` | 1–36 | Rank under gender-heavy model. |
| `rank_shift_gender` | `rank_baseline` − `rank_gender_focus` | Integer | Rank shift under gender priority. |

