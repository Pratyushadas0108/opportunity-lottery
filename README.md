# The Opportunity Lottery
**Measuring Geographic and Gender Disparities in Student Opportunity Across Indian States**

---

## 1. Problem Statement
How strongly is a student's access to opportunity associated with where they grow up in India?

Where a child is born and raised in India significantly influences their educational journey, career pathways, and economic mobility. Policymakers, philanthropic foundations, scholarship funds, and skilling organizations face resource allocation constraints: **where should capital and interventions be deployed first to maximize impact?**

*Note on Analytical Framing: This study measures statistical **association**, not causation. Differences between states represent structural links and concurrent patterns rather than direct cause-and-effect.*

---

## 2. Business Questions Answered
1. How do Indian states rank on overall student opportunity, and who sits in the top and bottom groups?
2. Do states with better school infrastructure also have better higher-education access and better youth job outcomes, or do gaps appear at specific stages?
3. Where does the gender gap widen most (literacy, school transition, higher-ed enrolment, workforce participation)?
4. Which states are outliers (e.g., strong schools but weak jobs; high female literacy but low female workforce participation)?
5. Can states be grouped into 3–4 "opportunity tiers", and what does each tier need most?
6. If a scholarship fund, skilling program, or school-funding scheme could start in only 5 states, which should they be and why?
7. How stable is the ranking if indicator weights change? (Sensitivity analysis)

---

## 3. Data Sources & Coverage
All indicators are sourced from official, public Government of India portals:
- **UDISE+ (Unified District Information System for Education Plus)**: School infrastructure, dropout rates, transition rates, pupil-teacher ratios.
- **AISHE (All India Survey on Higher Education)**: Gross Enrolment Ratio (GER), college density, Gender Parity Index.
- **PLFS (Periodic Labour Force Survey, MoSPI)**: Youth unemployment (15–29), labour force participation by gender, regular wage/salaried employment.
- **Census of India**: Baseline demographics, literacy rates, urban-rural population distribution.

---

## 4. Analytical Process & Index Methodology
The project synthesizes ~20 normalized indicators into four thematic sub-indices:
1. **School Access & Quality** (UDISE+)
2. **Higher-Education Access** (AISHE)
3. **Jobs & Economic Mobility** (PLFS)
4. **Gender Equality** (Cross-source)

- **Standardization**: Min-max normalization scaled from 0 to 100.
- **Directionality**: Inverted metrics where lower is better (e.g., dropout rates, unemployment).
- **Opportunity Index**: Equal-weight composite index of the four sub-indices, supported by sensitivity stress-testing.
- **Clustering**: K-Means clustering into distinct opportunity tiers.

---

## 5. Insights & Findings
*(To be authored by the analyst based on findings from the final data models).*

---

## 6. Strategic Recommendations
*(To be authored by the analyst based on analytical findings).*

---

## 7. Deliverables & Links
- **Interactive Opportunity Atlas**: *(GitHub Pages link to be added in Week 4)*
- **Data & Calculations**: `clean_data/state_master.csv`, `Opportunity_Lottery.xlsx`
- **Jupyter Notebooks**: `notebooks/`
- **Power BI Dashboard**: `dashboard/`

---

## 8. Limitations & Methodological Notes
1. **Temporal Asynchrony**: Data across government portals reflect different reporting years. All reporting years are explicitly tracked in data dictionaries.
2. **Ecological Fallacy / Intra-State Aggregation**: State-level averages mask significant intra-state and district-level disparities.
3. **Association vs. Causation**: High correlation between indicators does not prove direct causal mechanisms.

