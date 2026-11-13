# The Opportunity Lottery
### Assessing Student Opportunity Disparities Across Indian States & Union Territories

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Quality: 0 Nulls](https://img.shields.io/badge/Data%20Quality-0%20Nulls-brightgreen.svg)]()
[![States Covered: 36](https://img.shields.io/badge/States%20Covered-36%2F36-success.svg)]()
[![Live Atlas](https://img.shields.io/badge/Opportunity%20Atlas-Interactive%20Web%20App-orange.svg)](atlas/index.html)

**Analyst**: Pratyush Das (B.Tech Computer Science, AI/ML Specialization, Finance Minor)  
**Repository**: [github.com/Pratyushadas0108/opportunity-lottery](https://github.com/Pratyushadas0108/opportunity-lottery)

---

## 1. Executive Summary & Core Research Question

> **Core Research Question**: How strongly is a student's access to opportunity associated with where they grow up in India, and at what transition stages do disparities appear?

Where a child is born in India significantly influences their educational trajectory, career opportunities, and economic mobility. This project constructs an end-to-end analytical pipeline and composite **Opportunity Index** synthesizing over **40 indicators across all 36 Indian States and Union Territories** from four official government releases (UDISE+, AISHE, PLFS, and Census). 

### Methodological Rule: Association, Not Causation
All findings measure statistical **association**, not causation. Macro aggregate administrative data contains unobserved confounding variables (state fiscal policy, historical industrial clusters, geographic terrain, remittances). Relationships are described as co-occurring patterns rather than direct cause-and-effect.

---

## 2. Interactive Opportunity Atlas & Dashboards

- **Interactive Web App**: [Open Opportunity Atlas](atlas/index.html) — Filter rankings by region or entity type, inspect state profiles, and explore the gender funnel.
- **Power BI Dashboard Guide**: See [dashboard/powerbi_guide.md](dashboard/powerbi_guide.md) for DAX measures, Power Query steps, and the 4-page executive dashboard build specification.
- **Live Excel Model**: [Opportunity_Lottery.xlsx](Opportunity_Lottery.xlsx) — 100% dynamic native Excel formulas (`MIN`, `MAX`, `AVERAGE`, `INDEX`, `MATCH`) with zero hardcoded calculated cells.

---

## 3. Data Sources & Verified Reference Periods

Every indicator originates directly from official Government of India publications:

| Dataset | Issuing Body | Reference Period | Core Indicators Used |
| :--- | :--- | :---: | :--- |
| **UDISE+** | Department of School Education & Literacy, MoE | **Academic Year 2024–25** | Secondary Transition Rate, Secondary Dropout (by gender), PTR, % School Electricity, % Girls' Toilets, % Computers. |
| **AISHE** | Department of Higher Education, MoE | **Academic Year 2023–24** | College Gross Enrolment Ratio (GER 18–23), Gender Parity Index (GPI), Colleges per Lakh Population, College PTR. |
| **PLFS** | National Sample Survey Office (NSSO), MoSPI | **Calendar Year 2025** (Jan–Dec 2025) | Adult Literacy (7+), Labor Force Participation Rate (15+), Youth Unemployment Rate (15–29), Regular Salaried Share. |
| **Census** | Office of the Registrar General & Census Commissioner | **Census 2011** (1 March 2011) | Total Population, Sex Ratio, Proportion of Urban Population (%). |

*Click-by-click download steps and verification checklists are documented in [raw_data/README.md](raw_data/README.md) and [docs/data_sources_guide.md](docs/data_sources_guide.md).*

---

## 4. The Opportunity Index Framework

The composite Opportunity Index normalizes indicators on a **0 to 100 scale** using Min-Max scaling, with direction inversion ($100 - \text{scaled value}$) applied to "lower is better" metrics (e.g. dropouts, unemployment, student-teacher ratios).

$$\text{Opportunity Index} = 0.25(\text{School}) + 0.25(\text{Higher Ed}) + 0.25(\text{Jobs}) + 0.25(\text{Gender})$$

### Sensitivity Stress-Testing
To confirm rankings are not an artifact of equal weighting, the baseline model was evaluated against three alternative policy weighting schemes:
1. **Jobs-Heavy** (40% Jobs, 20% others): Spearman $\rho = +0.901$
2. **School-Heavy** (40% School, 20% others): Spearman $\rho = +0.938$
3. **Gender-Heavy** (40% Gender, 20% others): Spearman $\rho = +0.904$

**Verdict**: Spearman rank correlations remain **$\ge 0.901$ across all models**, confirming ranking stability.

---

## 5. Dual Rankings: All 36 Entities vs. 28 States Only

Small Union Territories (Chandigarh, Puducherry, D&NH and D&D) are compact and highly urbanized. To ensure fair comparison, rankings are provided across both frameworks:

### Framework A: All 36 States & Union Territories
- **Top 5**: 1. Chandigarh (`70.05`), 2. Puducherry (`68.81`), 3. Dadra & Nagar Haveli and Daman & Diu (`67.95`), 4. Sikkim (`67.36`), 5. Tamil Nadu (`64.92`).
- **Bottom 5**: 32. Manipur (`45.70`), 33. Jammu & Kashmir (`45.58`), 34. Meghalaya (`43.97`), 35. Arunachal Pradesh (`41.74`), 36. Bihar (`35.52`).
- **Divide**: Top 5 average (`67.82`) is **1.60x higher** than Bottom 5 average (`42.50`) — a 25.32-point absolute divide.

### Framework B: 28 States Only (Excluding Union Territories)
- **Top 5 States**: 1. **Sikkim** (`67.36`), 2. **Tamil Nadu** (`64.92` — **#1 major state**), 3. **Kerala** (`63.94`), 4. **Himachal Pradesh** (`63.57`), 5. **Karnataka** (`59.86`).
- **Top 6–10**: 6. Goa (`59.04`), 7. Gujarat (`58.04`), 8. Uttarakhand (`57.83`), 9. Haryana (`57.59`), 10. Maharashtra (`57.38`).
- **Bottom 5 States**: 24. Jharkhand (`46.35`), 25. Manipur (`45.70`), 26. Meghalaya (`43.97`), 27. Arunachal Pradesh (`41.74`), 28. Bihar (`35.52`).

---

## 6. The Analyst's Five Core Empirical Insights

#### 1. A 25-point gap separates the top and bottom of the opportunity index
Across 36 states and UTs, the top five average `67.8` and the bottom five `42.5`. Among the 28 full states, Sikkim ranks first, with Tamil Nadu as the highest-ranked large state, and Bihar is last at `35.5`. The ranking holds under three alternative weighting scenarios (four weighting schemes in total, Spearman $\rho \ge 0.90$).  
*Caveat: This is a relative index built from data across AY 2023–25, so it ranks states against each other and says nothing about absolute levels.*

#### 2. The gender gap appears at work, not in school
Girls drop out of secondary school less than boys (`9.6%` vs `13.3%`, UDISE+ AY 2024–25) and have a higher college enrolment ratio (`31.2` vs `28.9`, AISHE AY 2023–24). Yet male labour force participation is `79.1%` against `40.0%` for women, a `39.1` percentage point gap (PLFS CY 2025).  
*Caveat: These figures come from three different sources and reference periods, and workforce participation covers all women aged 15+, not only graduates.*

#### 3. Better school and college access go together, but neither lines up with youth job outcomes
School and higher-education scores are moderately correlated ($r = 0.51$), while higher-education access and youth job scores show almost no relationship ($r = 0.06$). Kerala ranks near the top for schools and colleges but 27th on jobs, with youth unemployment of about `20.8%`. Gujarat is first on jobs with `2.5%` youth unemployment, yet 21st in college enrolment.  
*Caveat: Only 36 observations, and half the jobs index is based on unemployment metrics. Educated youth searching for better jobs and out-migration are possible explanations that this cross-sectional data cannot test.*

#### 4. Two states can have the same score and need different help
Clusters 3 and 4 have nearly identical composite scores (`48.0` and `47.1`), but different shapes. The first (mostly northeastern and hill states) is relatively strong on gender (`55.2`) and weak on schools (`50.6`). The second (including Bihar, UP, and Rajasthan) has better schools (`62.0`) but the weakest higher education (`36.3`) and gender scores (`39.4`). Meghalaya shows the same pattern: a top-tier gender score (`64.8`) alongside school electrification of only `28.1%`.  
*Caveat: Clusters are statistical groupings from k-means with $k=4$ and are not official administrative categories.*

#### 5. Higher literacy and urbanization do not guarantee higher female labour participation
Delhi is `97.5%` urban with female literacy of `84.4%`, yet it has the lowest female labour force participation in the country at `13.1%`. Among full states, Haryana (`23.8%`) and Bihar (`24.7%`) are lowest.  
*Caveat: This describes a pattern in survey data, and the reasons (job availability, safety, social norms, how work is measured) are outside what this project tested.*

---

## 7. Actionable Policy Recommendations

Each intervention is computed from a single explicit column calculation in [clean_data/q6_targeted_interventions.csv](clean_data/q6_targeted_interventions.csv):

1. **Start school infrastructure funding in Meghalaya, Arunachal Pradesh, Bihar, Manipur, and Mizoram**:  
   They have the five lowest School Quality scores, and Meghalaya’s electrification figure (`28.1%`) shows basic physical facilities are the binding constraint. Check district-level data before allocating money, since state averages hide significant local variation.

2. **Focus college capacity and faculty funding on Bihar and Jharkhand first**:  
   They have the lowest higher-education access scores among large states, with Bihar showing `61.3` students per teacher and `8.07` colleges per lakh population. Small UTs on the same list (Ladakh, Andaman & Nicobar, D&NH and D&D) probably need different solutions, such as scholarships to study elsewhere or online and distance options, because they cannot support many standalone colleges.

3. **Pair skilling programs for women with job-access support in Delhi, Haryana, Bihar, Lakshadweep, and Goa**:  
   Female literacy is already high in several of them, so the data suggests the barrier lies after education. Start with targeted pilots, track formal employment outcomes, and test local constraints before scaling.

---

## 8. Repository Structure

```text
omnamahashivaya/
├── raw_data/                  # Untracked official downloads (README.md download steps)
├── clean_data/
│   ├── state_master.csv       # 36 States/UTs x 40 reconciled indicators (0 nulls)
│   ├── opportunity_index.csv  # Min-Max normalized sub-indices & sensitivity runs
│   ├── state_clusters.csv     # K-Means k=4 structural profiles
│   └── q6_targeted_interventions.csv # Explicitly calculated candidate state lists
├── notebooks/
│   ├── 01_cleaning.ipynb      # PDF/Excel extraction & name reconciliation
│   ├── 02_index_building.ipynb # Normalization, weighting & sensitivity
│   └── 03_analysis.ipynb      # Correlations, clustering, gap analysis
├── dashboard/
│   ├── opportunity_powerbi_data.csv # Denormalized Power BI export
│   ├── powerbi_guide.md       # DAX measures & visual layout specs
│   └── charts/                # 6 presentation-ready charts
├── atlas/
│   └── index.html             # Standalone interactive Opportunity Atlas
├── docs/
│   ├── findings_table.md      # Complete empirical findings and insights
│   ├── data_dictionary.md     # Indicator definitions, directionality & formulas
│   ├── data_quality.md        # Audit verification & zero-null log
│   └── assumptions_log.md     # Audit trail of methodological decisions
├── scripts/                   # Automated audit & pipeline scripts
├── interview_notes.txt        # 500+ line interview defense compendium
└── Opportunity_Lottery.xlsx   # Dynamic Excel model with live formulas
```

---

## 9. How to Reproduce

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pratyushadas0108/opportunity-lottery.git
   cd opportunity-lottery
   ```
2. **Set up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install pandas numpy openpyxl scipy matplotlib seaborn pypdf pdfplumber
   ```
3. **Execute Analysis & Visualizations**:
   ```bash
   python scripts/run_analysis.py
   python scripts/prepare_dashboard_data.py
   python scripts/build_atlas.py
   ```
4. **Open Opportunity Atlas**:
   Double click `atlas/index.html` in your browser.

---

## 10. License & Author Note

Distributed under the **MIT License**.  
This project was designed and built as a personal data analyst portfolio project adhering strictly to government data governance standards and empirical association framing.
