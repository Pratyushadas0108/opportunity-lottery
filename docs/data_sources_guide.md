# Official Data Sources Guide & Download Checklist

This guide gives the official government portal, report name, table reference, expected file format, and step-by-step instructions for downloading the raw datasets needed for **The Opportunity Lottery**.

Follow the click-by-click instructions. Place every downloaded file into `raw_data/` without modifying it.

---

## 1. UDISE+ (Unified District Information System for Education Plus)
- **Ministry / Agency**: Department of School Education and Literacy, Ministry of Education, Government of India.
- **Official Portal**: [udiseplus.gov.in](https://udiseplus.gov.in)
- **Key Navigation**: Navigate to **Publications / Reports** (or go to `udiseplus.gov.in/#/publications`).
- **Target Report**: *UDISE+ Flash Statistics 2021-22* or *State-wise School Education Statistics (2021-22 or 2022-23)*.
- **Indicators to extract**:
  1. Percentage of schools with functional electricity by State/UT.
  2. Percentage of schools with functional girls' toilets by State/UT.
  3. Percentage of schools with functional computers / ICT labs by State/UT.
  4. Pupil-Teacher Ratio (PTR) at Secondary level by State/UT.
  5. Annual average dropout rate at secondary level (Class IX–X) by State/UT and gender.
  6. Transition rate from Upper Primary to Secondary schooling by State/UT.
- **Expected Format**: Excel (`.xlsx`) if table download is available, or PDF tables (which we will extract using Python).
- **Status**: *Verify latest year and format on portal*.

---

## 2. AISHE (All India Survey on Higher Education)
- **Ministry / Agency**: Department of Higher Education, Ministry of Education, Government of India.
- **Official Portal**: [aishe.gov.in](https://aishe.gov.in)
- **Key Navigation**: Go to **Reports** → **All India Survey on Higher Education Report** (e.g. 2021-22 or 2022-23).
- **Target Tables / Statements**:
  1. *Gross Enrolment Ratio (GER) in Higher Education (18–23 years)* by State/UT, for Male, Female, and Total.
  2. *Gender Parity Index (GPI)* in Higher Education (18–23 years) by State/UT.
  3. *College Density*: Number of Colleges per lakh (100,000) population (18–23 years) by State/UT.
  4. *Pupil-Teacher Ratio (PTR)* in Universities and Colleges by State/UT (*verify on portal*).
- **Expected Format**: PDF report tables or downloadable Annexure Excel sheets.
- **Status**: *Verify latest published annual report on portal*.

---

## 3. PLFS (Periodic Labour Force Survey)
- **Ministry / Agency**: National Sample Survey Office (NSSO), Ministry of Statistics and Programme Implementation (MoSPI).
- **Official Portal**: [mospi.gov.in](https://mospi.gov.in) (Reports & Publications section) or [microdata.gov.in](https://microdata.gov.in).
- **Target Report**: *Annual Report: Periodic Labour Force Survey (July 2022 – June 2023)* or *July 2023 – June 2024*.
- **Target Statements (State-wise Summary Tables)**:
  1. *Unemployment Rate (UR)* according to Usual Status (ps+ss) for youth aged 15–29 years by State/UT (Male, Female, Person).
  2. *Labour Force Participation Rate (LFPR)* according to Usual Status (ps+ss) for youth aged 15–29 years and age 15+ by State/UT (Male, Female, Person).
  3. *Percentage distribution of usually working persons (ps+ss)* by broad status in employment (Regular Wage / Salaried share) by State/UT.
  4. *Overall Unemployment Rate (all ages, ps+ss)* by State/UT.
- **Expected Format**: PDF Statistical Statements or Annexure Excel tables.
- **Status**: *Verify latest annual report statements on MoSPI portal*.

---

## 4. Census of India (Demographic Baseline)
- **Ministry / Agency**: Office of the Registrar General & Census Commissioner, India (ORGI), Ministry of Home Affairs.
- **Official Portal**: [censusindia.gov.in](https://censusindia.gov.in) or [data.gov.in](https://data.gov.in).
- **Target Table**: *Primary Census Abstract (PCA) 2011 (State/UT level)* or *State-wise Literacy Rates Table*.
- **Indicators to extract**:
  1. Total Population, Male Population, Female Population.
  2. Rural Population, Urban Population (Urbanization rate %).
  3. Total Literacy Rate, Male Literacy Rate, Female Literacy Rate.
  4. Gender gap in literacy (Male % − Female %).
- **Expected Format**: Excel (`.xls` / `.xlsx`) or CSV.
- **Status**: *Standard historical baseline (2011)*.

---

## Download Checklist & Workflow
| Source | Downloaded? | Raw File Name in `raw_data/` | Verified with Agent? | Reference Year |
| :--- | :---: | :--- | :---: | :---: |
| **UDISE+** | [ ] | *(e.g. udise_2021_22_raw.xlsx)* | [ ] | |
| **AISHE** | [ ] | *(e.g. aishe_2021_22_raw.xlsx)* | [ ] | |
| **PLFS** | [ ] | *(e.g. plfs_2022_23_raw.pdf / .xlsx)* | [ ] | |
| **Census 2011** | [ ] | *(e.g. census_2011_pca_raw.xlsx)* | [ ] | 2011 |
