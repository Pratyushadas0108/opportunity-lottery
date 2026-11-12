# Assumptions & Methodological Decisions Log

This document serves as an immutable audit trail for all data transformations, state-name standardizations, boundary adjustments, and analytical decisions made throughout **The Opportunity Lottery**.

Every entry must record:
- **Date / Timestamp**
- **Decision Category** (State Mapping, Missing Values, Indicator Selection, Normalization)
- **Problem Statement**
- **Decision Taken**
- **Methodological Justification** (Defense for interview / stakeholder review)

---

## Initial Methodological Assumptions

### Log Entry 001: Association vs. Causation
- **Date**: 2026-11-13
- **Category**: Analytical Framing
- **Decision**: All findings, visual labels, and narrative descriptions must state statistical **association**, never causation.
- **Justification**: Observational aggregate data across macro administrative units cannot control for all unobserved confounders (e.g., historical state fiscal expenditure, private industry concentration, migration dynamics). Framing relationships as associations ensures scientific accuracy and interview credibility.

---

### Log Entry 002: Spatial Unit of Analysis (Phase 1)
- **Date**: 2026-11-13
- **Category**: Scope
- **Decision**: Phase 1 index is calculated at the State and Union Territory level (36 entities).
- **Justification**: Periodic Labour Force Survey (PLFS) sampling is statistically representative and stratified at the State/UT level. Reporting PLFS employment estimates at district level yields high standard errors and unrepresentative sample sizes.

---

### Log Entry 003: Administrative Boundary Changes Post-Census 2011
- **Date**: 2026-11-13
- **Category**: State Mapping & Boundary Harmonization
- **Decisions**:
  1. **Telangana & Andhra Pradesh**: Census 2011 reported undivided Andhra Pradesh. For Census baseline measures (e.g. 2011 population/literacy), district-level aggregation from Census 2011 district tables will be used to reconstruct exact pre-bifurcation boundaries for modern Andhra Pradesh and Telangana, OR modern PLFS/UDISE estimates will be preferred.
  2. **Jammu & Kashmir and Ladakh**: Split into two UTs in October 2019. Modern UDISE+, AISHE, and PLFS report them separately. For Census 2011 baselines, Leh and Kargil districts constitute Ladakh, and remaining districts constitute Jammu & Kashmir.
  3. **Dadra & Nagar Haveli and Daman & Diu**: Formally merged into a single UT in January 2020. Where older reports list them separately, weighted averages by population will be used to reconcile into the unified entity.
- **Justification**: Cross-sectional index requires a harmonized spatial unit set representing modern administrative realities.

---

### Log Entry 004: Indicator Directionality & Inversion Formula
- **Date**: 2026-11-13
- **Category**: Index Construction
- **Decision**: All indicators are scaled 0–100 via Min-Max. For "lower is better" indicators (e.g., secondary dropout rate, youth unemployment rate, literacy gender gap), the score is inverted using $100 - \text{scaled value}$.
- **Justification**: Ensures that across all 4 sub-indices and the final Opportunity Index, a higher numerical score consistently represents greater opportunity and welfare for students.

---

### Log Entry 005: Equal-Weighted Arithmetic Index Formulation
- **Date**: 2026-11-13
- **Category**: Weighting
- **Decision**: Baseline Opportunity Index applies equal weights (25% each) across the 4 thematic sub-indices, followed by explicit sensitivity analysis with 3 alternative weighting scenarios (Jobs-heavy, School-heavy, Gender-heavy).
- **Justification**: Prevents subjective normative bias in the core benchmark while systematically demonstrating ranking robustness under sensitivity testing.



---

## Verified Raw Datasets Inventory

### Log Entry 006: Verification of Official Datasets
- **Date**: 2026-11-13
- **Category**: Data Verification & Provenance

1. **UDISE+ School Education Dataset**:
   - **File**: `raw_data/UDISE+2024_25_Booklet_existing.118ba29d4773e6372f72.pdf`
   - **Year**: 2024–25 (Latest official booklet)
   - **Source**: Department of School Education & Literacy, Ministry of Education
   - **Tables Verified**:
     - Table 4.12 (p. 63): Pupil-Teacher Ratio (PTR) Secondary
     - Table 6.13 (p. 120): Secondary Dropout Rate (Total, Boys, Girls)
     - Table 6.14 (p. 121): Upper Primary to Secondary Transition Rate
     - Table 8.6 (p. 161): % Functional Electricity (All management)
     - Table 8.8 (p. 163): % Functional Girls' Toilet (All management)
     - Table 7.10 (p. 138): % Functional Computer facility for pedagogical purposes
     - Table 7.11 (p. 139): % Internet facility available

2. **AISHE Higher Education Dataset**:
   - **File**: `raw_data/AISHE Final Report 2023-24.xlsx`
   - **Year**: 2023–24 (Latest official release)
   - **Source**: Department of Higher Education, Ministry of Education
   - **Sheets Verified**:
     - `19GER(2011)`: Gross Enrolment Ratio (Male, Female, Total)
     - `20GPI2011`: Gender Parity Index in Higher Education
     - `4CollegeIndicator`: Colleges per lakh population & average college enrolment
     - `25PTR`: Pupil-Teacher Ratio in regular mode higher education

3. **PLFS Employment & Labour Dataset**:
   - **File**: `raw_data/Annual_Report_PLFS_2025.pdf`
   - **Year**: Calendar Year 2025 (January–December 2025)
   - **Source**: National Sample Survey Office (NSSO), MoSPI
   - **Tables Verified**:
     - Table 18.0 (p. 152): Youth Unemployment Rate (15–29 years, Usual Status ps+ss) for Total, Male, Female
     - Table 18.0 (p. 155): Overall Unemployment Rate (all ages)
     - Table 16.0 (p. 142): Youth LFPR (15–29 years)
     - Table 16.0 (p. 144): Female LFPR (15+ years)
     - Table 19 (p. 157–165): Regular wage / salaried employment share

4. **Census of India Demographic Baseline**:
   - **File**: `raw_data/2011-IndiaState-0000.xlsx`
   - **Year**: 2011 (Official Primary Census Abstract - State Level)
   - **Source**: Office of the Registrar General & Census Commissioner, India
   - **Metrics Verified**: Total Population (`TOT_P`), Male (`TOT_M`), Female (`TOT_F`), Population 0–6 (`P_06`, `M_06`, `F_06`), Literate Population (`P_LIT`, `M_LIT`, `F_LIT`).
