# Raw Data Directory & Reproduction Guide

To keep the git repository lightweight and fast to clone, raw government survey publications (~47 MB total) are stored locally in this folder and ignored by Git (`.gitignore`).

Anyone cloning this repository can reproduce the raw dataset inventory by downloading the exact official files described below and placing them into `raw_data/`.

---

## Official Dataset Catalog & Download Steps

### 1. UDISE+ School Education Statistics
- **Portal Name**: Unified District Information System for Education Plus (UDISE+), Ministry of Education
- **Direct Portal URL**: [https://udiseplus.gov.in/#/publications](https://udiseplus.gov.in/#/publications)
- **Exact File Name**: `UDISE+2024_25_Booklet_existing.118ba29d4773e6372f72.pdf`
- **Dataset Reference Year**: 2024–25
- **Download Date**: 2026-11-13
- **File Size**: ~11.8 MB (189 pages)
- **Step-by-Step Instructions**:
  1. Navigate to `https://udiseplus.gov.in/#/publications` (or search Google for `UDISE+ 2024-25 booklet filetype:pdf`).
  2. No login is needed: locate the public report *UDISE+ 2024-25 Key Results / Booklet*.
  3. Click the download icon to save the PDF.
  4. Save the file into `raw_data/UDISE+2024_25_Booklet_existing.118ba29d4773e6372f72.pdf`.

---

### 2. AISHE Higher Education Statistics
- **Portal Name**: All India Survey on Higher Education (AISHE), Ministry of Education
- **Direct Portal URL**: [https://aishe.gov.in](https://aishe.gov.in)
- **Exact File Name**: `AISHE Final Report 2023-24.xlsx`
- **Dataset Reference Year**: 2023–24
- **Download Date**: 2026-11-13
- **File Size**: ~785 KB (51 statistical sheets)
- **Step-by-Step Instructions**:
  1. Navigate to `https://aishe.gov.in` under Reports / Public Downloads (or search Google for `AISHE Final Report 2023-24 excel`).
  2. Download the official statistical tables workbook containing Statements 4, 19, 20, and 25.
  3. Save the file into `raw_data/AISHE Final Report 2023-24.xlsx`.

---

### 3. PLFS Employment & Labour Statistics
- **Portal Name**: Periodic Labour Force Survey (PLFS), National Sample Survey Office (NSSO), MoSPI
- **Direct Portal URL**: [https://mospi.gov.in](https://mospi.gov.in)
- **Exact File Name**: `Annual_Report_PLFS_2025.pdf`
- **Dataset Reference Year**: Calendar Year 2025 (January – December 2025)
- **Download Date**: 2026-11-13
- **File Size**: ~34.6 MB (653 pages)
- **Step-by-Step Instructions**:
  1. Navigate to `https://mospi.gov.in` under Reports & Publications → Labour Force Statistics (or search Google for `Annual Report PLFS 2025 pdf mospi`).
  2. Locate and download the complete Annual Report covering Calendar Year 2025.
  3. Save the file into `raw_data/Annual_Report_PLFS_2025.pdf`.

---

### 4. Census of India 2011 (Demographic Baseline)
- **Portal Name**: Office of the Registrar General & Census Commissioner, India (ORGI) / Open Government Data Platform
- **Direct Portal URL**: [https://censusindia.gov.in](https://censusindia.gov.in) / [https://data.gov.in](https://data.gov.in)
- **Exact File Name**: `2011-IndiaState-0000.xlsx`
- **Dataset Reference Year**: 2011
- **Download Date**: 2026-11-13
- **File Size**: ~90 KB
- **Step-by-Step Instructions**:
  1. Navigate to `https://censusindia.gov.in` → Data Products → Primary Census Abstract (PCA) State Level Table (or search Google for `census 2011 primary census abstract state total excel filetype:xlsx`).
  2. Download the state-level demographic and literacy summary spreadsheet.
  3. Save the file into `raw_data/2011-IndiaState-0000.xlsx`.

---

## Immutability Rule
Files placed in this `raw_data/` folder are strictly read-only. All transformations, filtering, and metric derivations are performed via automated scripts that output exclusively to `clean_data/`.

