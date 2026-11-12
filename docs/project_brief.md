# Project Brief: The Opportunity Lottery
**Measuring Geographic and Gender Disparities in Student Opportunity Across Indian States**

---

## 1. Executive Summary & Core Research Question
**How strongly is a student's access to opportunity associated with where they grow up in India?**

In India, a young person's educational progression and entry into productive employment are heavily influenced by the state in which they reside. This project constructs an empirical, multi-dimensional **Opportunity Index** to quantify educational infrastructure, higher-education access, labor market outcomes, and gender parity across Indian States and Union Territories.

### ⚠️ Methodological Ground Rule: Association vs. Causation
This study evaluates **statistical association**, **not causation**. 
- **Permissible phrasing**: *"is associated with"*, *"tends to coincide with"*, *"is linked to"*, *"co-occurs with"*.
- **Prohibited phrasing**: *"causes"*, *"leads to"*, *"drives"*, *"results in"*.
In data analyst interviews, defending this distinction demonstrates statistical maturity and prevents over-interpreting aggregate observational data.

---

## 2. Business Context & Stakeholder Relevance
Who cares about this data and why?
- **State & Central Policymakers**: Identifying which public interventions (school facilities vs. higher-ed capacity vs. job creation) correlate with overall youth mobility.
- **Philanthropic Foundations & Scholarship Funds**: Prioritizing resource allocation to states with high educational aspiration but severe structural bottlenecks.
- **EdTech & Vocational Skilling Organizations**: Pinpointing geographic markets with high school completion but low college enrolment or severe youth unemployment.
- **Corporate Social Responsibility (CSR) Heads**: Designing targeted, location-sensitive skill development programs.

---

## 3. Seven Core Business Questions
1. **State Rankings**: How do Indian states rank on overall student opportunity, and who sits in the top and bottom groups?
2. **Transition Bottlenecks**: Do states with better school infrastructure also have better higher-education access and better youth job outcomes, or do drop-offs appear at specific transition stages?
3. **Gender Divide Across the Pipeline**: Where does the gender gap widen most (literacy, school transition, higher-ed enrolment, or labor force participation)?
4. **Outlier Identification**: Which states defy standard expectations (e.g., strong schools but weak employment; high female literacy but low female workforce participation)?
5. **Opportunity Tiers (Clustering)**: Can states be grouped into 3–4 distinct "opportunity tiers" using unsupervised learning, and what specific intervention does each tier need most?
6. **Capital Allocation Priority**: If a scholarship fund, skilling program, or school infrastructure initiative could launch in only 5 states, which states should be selected and on what empirical basis?
7. **Robustness & Sensitivity**: How stable is the state ranking if indicator weights change across different stakeholder priorities?

---

## 4. Scope & Granularity
- **Phase 1 (Primary Analysis)**: State and Union Territory level (~36 states/UTs). This level aligns with the reporting granularity of the Periodic Labour Force Survey (PLFS).
- **Phase 2 (Deep Dive - Optional)**: District-level analysis for 2–3 contrasting states using UDISE+, AISHE, and Census metrics.
- **Indicator Economy**: Keep the index focused and interpretable: 4–6 robust indicators per theme (~20 indicators total), avoiding noisy, high-dimensional indicator lists.

---

## 5. Index Architecture & Methodology
The composite **Opportunity Index** is constructed from four thematic sub-indices:
1. **School Access and Quality** (UDISE+)
2. **Higher-Education Access** (AISHE)
3. **Jobs and Economy** (PLFS)
4. **Gender Equality** (Cross-source synthesis)

### Mathematical Formulation
1. **Min-Max Normalization (0–100 scale)**:
   For "Higher is Better" indicators ($X$):
   $$S = \frac{X - X_{\min}}{X_{\max} - X_{\min}} \times 100$$
2. **Direction Inversion**:
   For "Lower is Better" indicators (e.g., dropout rates, youth unemployment):
   $$S_{\text{inverted}} = 100 - S = \frac{X_{\max} - X}{X_{\max} - X_{\min}} \times 100$$
3. **Thematic Sub-Index**:
   Equal-weighted arithmetic mean of normalized indicators within that theme.
4. **Composite Opportunity Index**:
   Equal-weighted arithmetic mean of the four sub-indices:
   $$\text{Opportunity Index} = \frac{1}{4} \sum_{i=1}^4 \text{SubIndex}_i$$
5. **Sensitivity Stress Testing**:
   Evaluation against alternative weighting models (e.g., jobs-heavy, schooling-heavy, gender-prioritized).

---

## 6. Official Data Sources
- **UDISE+** (Unified District Information System for Education Plus, Ministry of Education): School infrastructure, pupil-teacher ratios, girls' sanitation, ICT access, transition and dropout rates.
- **AISHE** (All India Survey on Higher Education, Ministry of Education): Gross Enrolment Ratio (GER), college density per lakh population, Gender Parity Index in tertiary education.
- **PLFS** (Periodic Labour Force Survey, MoSPI): Labor Force Participation Rate (LFPR), Worker Population Ratio (WPR), youth unemployment rate (15–29), salaried/regular wage share.
- **Census of India**: State base populations, overall/female literacy, rural-urban population ratios.

---

## 7. Operating Rules & Governance
- **Data Integrity**: Zero invented, synthetic, or memorized figures. Every data point must trace to an official raw download.
- **Raw Data Immutability**: Files in `raw_data/` are read-only. All transformations write strictly to `clean_data/`.
- **Temporal Transparency**: Data collection years vary across government sources; each dataset's reference year must be explicitly documented in logs and dictionaries.
- **Audit Trail**: Every state name standardization, boundary merge (e.g., Dadra & Nagar Haveli and Daman & Diu), and missing-value treatment must be logged in `docs/assumptions_log.md`.
- **Analyst Authorship**: The analysis agent provides empirical tables, charts, and models; final narrative insights and strategic recommendations are authored by the student.
