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
