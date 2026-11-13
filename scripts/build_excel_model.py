"""
The Opportunity Lottery - Excel Workbook Generator
Constructs Opportunity_Lottery.xlsx with:
1. Notes (Metadata, Sources, Years, Methodology)
2. Raw_Summary (Catalog of raw tables and variables)
3. Clean (Clean state master data)
4. Normalized (Live Min-Max formulas referencing Clean sheet)
5. Index (Live Excel formulas for Sub-Indices, Composite Index, Rankings, and Sensitivity Scenarios)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

# Load clean datasets
df_master = pd.read_csv('clean_data/state_master.csv')
df_index = pd.read_csv('clean_data/opportunity_index.csv')

wb = openpyxl.Workbook()

# Style definitions
font_title = Font(name='Calibri', size=16, bold=True, color='1F497D')
font_subtitle = Font(name='Calibri', size=11, italic=True, color='595959')
font_header = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
font_bold = Font(name='Calibri', size=11, bold=True)
font_regular = Font(name='Calibri', size=11)

fill_navy = PatternFill(start_color='1F497D', end_color='1F497D', fill_type='solid')
fill_soft_blue = PatternFill(start_color='DCE6F1', end_color='DCE6F1', fill_type='solid')
fill_accent = PatternFill(start_color='EDF2F8', end_color='EDF2F8', fill_type='solid')
fill_header_green = PatternFill(start_color='2E75B6', end_color='2E75B6', fill_type='solid')

border_thin = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
border_header = Border(
    left=Side(style='thin', color='1F497D'),
    right=Side(style='thin', color='1F497D'),
    top=Side(style='medium', color='1F497D'),
    bottom=Side(style='medium', color='1F497D')
)

# -------------------------------------------------------------
# SHEET 1: Notes
# -------------------------------------------------------------
ws_notes = wb.active
ws_notes.title = 'Notes'
ws_notes.views.sheetView[0].showGridLines = True

ws_notes['A1'] = "THE OPPORTUNITY LOTTERY: MODEL DOCUMENTATION & AUDIT LOG"
ws_notes['A1'].font = font_title
ws_notes['A2'] = "Measuring Geographic and Gender Disparities in Student Opportunity Across Indian States"
ws_notes['A2'].font = font_subtitle

notes_content = [
    ("1. Core Research Question", "How strongly is a student's access to opportunity associated with where they grow up in India?"),
    ("2. Association vs. Causation", "This study evaluates statistical association, not causation. High correlations indicate spatial co-occurrence, not direct causal links."),
    ("3. Official Data Sources", "1) UDISE+ 2024-25 (MoE): School Infrastructure & Quality\n2) AISHE 2023-24 (MoE): Higher-Education Access\n3) PLFS 2025 Calendar Year (MoSPI): Employment, LFPR & Modern Literacy\n4) Census of India 2011 (ORGI): Demographic Baselines"),
    ("4. Index Methodology", "• Indicators scaled 0-100 via Min-Max.\n• Lower-is-better metrics inverted (100 - scaled value).\n• Four thematic sub-indices calculated as arithmetic means.\n• Composite Opportunity Index is equal-weighted (25% each sub-index)."),
    ("5. Live Formulas", "Sheets 'Normalized' and 'Index' contain 100% dynamic live Excel formulas referencing the 'Clean' data sheet."),
    ("6. Sensitivity Scenarios", "Includes 3 stress-testing models: Jobs-heavy (40%), Schooling-heavy (40%), and Gender-heavy (40%)."),
    ("7. Licensing & Redistribution", "Official Government of India Open Data publications under NDSAP / Section 52(1)(q)(iv) of Indian Copyright Act 1957.")
]

row_idx = 4
for heading, body in notes_content:
    ws_notes.cell(row=row_idx, column=1, value=heading).font = font_bold
    ws_notes.cell(row=row_idx, column=1).fill = fill_soft_blue
    ws_notes.cell(row=row_idx+1, column=1, value=body).font = font_regular
    ws_notes.cell(row=row_idx+1, column=1).alignment = Alignment(wrap_text=True)
    row_idx += 3

ws_notes.column_dimensions['A'].width = 110

# -------------------------------------------------------------
# SHEET 2: Raw_Summary
# -------------------------------------------------------------
ws_raw = wb.create_sheet(title='Raw_Summary')
ws_raw.views.sheetView[0].showGridLines = True

ws_raw['A1'] = "RAW DATA INVENTORY & VERIFICATION SUMMARY"
ws_raw['A1'].font = font_title

raw_headers = ["Domain", "Source Agency", "Publication / Report", "Reference Year", "Raw Format & Size", "Verified Indicators"]
for c_idx, h in enumerate(raw_headers, 1):
    c = ws_raw.cell(row=3, column=c_idx, value=h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = Alignment(horizontal='center', vertical='center')

raw_rows = [
    ["School Education", "Ministry of Education (MoE)", "UDISE+ 2024-25 Booklet", "2024-25", "PDF (11.8 MB)", "Secondary PTR, Secondary Dropout Rate (Total/Boys/Girls), Transition Rate Upper Prim to Sec, % Functional Electricity, % Functional Girls Toilets, % Functional Computers, % Internet"],
    ["Higher Education", "Ministry of Education (MoE)", "AISHE Final Report 2023-24", "2023-24", "Excel (785 KB)", "Gross Enrolment Ratio (GER Male/Female/Total), Gender Parity Index (GPI), Colleges per Lakh Population (18-23), College Average Enrolment, Higher-Ed PTR"],
    ["Jobs & Economy", "National Sample Survey Office (MoSPI)", "Annual Report: PLFS 2025", "Calendar 2025", "PDF (34.6 MB)", "Youth Unemployment Rate (15-29 Total/Male/Female), Overall Unemployment Rate, Youth LFPR (15-29), Female LFPR (15+), Regular Wage/Salaried Share, Modern Literacy Rates"],
    ["Demographics", "Registrar General & Census Commissioner (MHA)", "Census 2011 Primary Census Abstract", "2011", "Excel (90 KB)", "Total Population, Male/Female Population, Urban Population Share (%), 2011 Historical Literacy Rates"]
]

for r_idx, row_data in enumerate(raw_rows, 4):
    for c_idx, val in enumerate(row_data, 1):
        c = ws_raw.cell(row=r_idx, column=c_idx, value=val)
        c.font = font_regular
        c.border = border_thin
        c.alignment = Alignment(wrap_text=True, vertical='top')

col_widths_raw = [18, 28, 30, 16, 18, 55]
for idx, w in enumerate(col_widths_raw, 1):
    ws_raw.column_dimensions[get_column_letter(idx)].width = w

# -------------------------------------------------------------
# SHEET 3: Clean (State Master Data)
# -------------------------------------------------------------
ws_clean = wb.create_sheet(title='Clean')
ws_clean.views.sheetView[0].showGridLines = True

# Select 20 core index indicators + state identifiers
clean_cols = [
    'state_code', 'state_name', 'entity_type',
    # School
    'ptr_secondary', 'dropout_sec_total', 'transition_rate_upprim_to_sec',
    'pct_schools_electricity', 'pct_schools_girls_toilet', 'pct_schools_computers',
    # Higher Ed
    'ger_higher_ed_total', 'colleges_per_lakh_pop', 'avg_enrolment_per_college', 'ptr_higher_ed',
    # Jobs
    'youth_unemployment_rate_15_29', 'overall_unemployment_rate', 'youth_lfpr_15_29', 'regular_wage_salaried_share',
    # Gender
    'gpi_higher_ed', 'female_lfpr_15_plus', 'female_literacy_rate_plfs',
    'literacy_gender_gap_plfs', 'youth_female_unemployment_rate', 'dropout_sec_gender_gap'
]

df_clean_export = df_master[clean_cols].sort_values(by='state_name').reset_index(drop=True)

for col_idx, col_name in enumerate(clean_cols, 1):
    cell = ws_clean.cell(row=1, column=col_idx, value=col_name)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = border_header

for r_idx, row_vals in enumerate(df_clean_export.values, 2):
    for c_idx, val in enumerate(row_vals, 1):
        cell = ws_clean.cell(row=r_idx, column=c_idx, value=val)
        cell.font = font_regular
        cell.border = border_thin
        if c_idx > 3:
            cell.number_format = '0.00'
            cell.alignment = Alignment(horizontal='right')
        else:
            cell.alignment = Alignment(horizontal='left')

for c_idx in range(1, len(clean_cols) + 1):
    ws_clean.column_dimensions[get_column_letter(c_idx)].width = 18
ws_clean.column_dimensions['B'].width = 32

# -------------------------------------------------------------
# SHEET 4: Normalized (LIVE EXCEL MIN-MAX FORMULAS)
# -------------------------------------------------------------
ws_norm = wb.create_sheet(title='Normalized')
ws_norm.views.sheetView[0].showGridLines = True

# Directions map: True = lower is better (flip), False = higher is better
inverted_cols = {
    'ptr_secondary': True,
    'dropout_sec_total': True,
    'transition_rate_upprim_to_sec': False,
    'pct_schools_electricity': False,
    'pct_schools_girls_toilet': False,
    'pct_schools_computers': False,
    'ger_higher_ed_total': False,
    'colleges_per_lakh_pop': False,
    'avg_enrolment_per_college': False,
    'ptr_higher_ed': True,
    'youth_unemployment_rate_15_29': True,
    'overall_unemployment_rate': True,
    'youth_lfpr_15_29': False,
    'regular_wage_salaried_share': False,
    'gpi_higher_ed': False,
    'female_lfpr_15_plus': False,
    'female_literacy_rate_plfs': False,
    'literacy_gender_gap_plfs': True,
    'youth_female_unemployment_rate': True,
    'dropout_sec_gender_gap': True
}

# Headers for Normalized sheet
for c_idx, col_name in enumerate(clean_cols, 1):
    header_text = f"norm_{col_name}" if c_idx > 3 else col_name
    cell = ws_norm.cell(row=1, column=c_idx, value=header_text)
    cell.font = font_header
    cell.fill = fill_header_green
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = border_header

# Populate Live Formulas
total_rows = len(df_clean_export)
for r_idx in range(2, total_rows + 2):
    # Identifiers reference Clean sheet
    ws_norm.cell(row=r_idx, column=1, value=f"=Clean!A{r_idx}").font = font_regular
    ws_norm.cell(row=r_idx, column=2, value=f"=Clean!B{r_idx}").font = font_regular
    ws_norm.cell(row=r_idx, column=3, value=f"=Clean!C{r_idx}").font = font_regular
    
    for c_idx in range(4, len(clean_cols) + 1):
        col_letter = get_column_letter(c_idx)
        raw_col_name = clean_cols[c_idx - 1]
        is_inverted = inverted_cols[raw_col_name]
        
        # Live Min-Max Formula
        # (Clean!X2 - MIN(Clean!X$2:X$37)) / (MAX(Clean!X$2:X$37) - MIN(Clean!X$2:X$37)) * 100
        min_expr = f"MIN(Clean!{col_letter}$2:{col_letter}${total_rows+1})"
        max_expr = f"MAX(Clean!{col_letter}$2:{col_letter}${total_rows+1})"
        val_expr = f"Clean!{col_letter}{r_idx}"
        
        if is_inverted:
            formula = f"=ROUND(100 - (({val_expr} - {min_expr}) / ({max_expr} - {min_expr}) * 100), 2)"
        else:
            formula = f"=ROUND((({val_expr} - {min_expr}) / ({max_expr} - {min_expr}) * 100), 2)"
            
        cell = ws_norm.cell(row=r_idx, column=c_idx, value=formula)
        cell.font = font_regular
        cell.number_format = '0.00'
        cell.border = border_thin
        cell.alignment = Alignment(horizontal='right')

for c_idx in range(1, len(clean_cols) + 1):
    ws_norm.column_dimensions[get_column_letter(c_idx)].width = 18
ws_norm.column_dimensions['B'].width = 32

# -------------------------------------------------------------
# SHEET 5: Index (LIVE SUB-INDICES, COMPOSITE & SENSITIVITY FORMULAS)
# -------------------------------------------------------------
ws_index = wb.create_sheet(title='Index')
ws_index.views.sheetView[0].showGridLines = True

index_headers = [
    "State Code", "State Name", "Entity Type",
    "School Sub-Index", "Higher-Ed Sub-Index", "Jobs Sub-Index", "Gender Sub-Index",
    "Opportunity Index", "Rank (Baseline)",
    "Index (Jobs Focus)", "Rank (Jobs Focus)",
    "Index (School Focus)", "Rank (School Focus)",
    "Index (Gender Focus)", "Rank (Gender Focus)"
]

for c_idx, h in enumerate(index_headers, 1):
    cell = ws_index.cell(row=1, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = border_header

# In Normalized sheet:
# School cols: col 4 to 9 (D to I)
# Higher Ed cols: col 10 to 13 (J to M)
# Jobs cols: col 14 to 17 (N to Q)
# Gender cols: col 18 to 23 (R to W)

for r_idx in range(2, total_rows + 2):
    # State identifiers
    ws_index.cell(row=r_idx, column=1, value=f"=Normalized!A{r_idx}").font = font_regular
    ws_index.cell(row=r_idx, column=2, value=f"=Normalized!B{r_idx}").font = font_bold
    ws_index.cell(row=r_idx, column=3, value=f"=Normalized!C{r_idx}").font = font_regular
    
    # Sub-indices (live AVERAGE formulas referencing Normalized sheet)
    ws_index.cell(row=r_idx, column=4, value=f"=ROUND(AVERAGE(Normalized!D{r_idx}:I{r_idx}), 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=5, value=f"=ROUND(AVERAGE(Normalized!J{r_idx}:M{r_idx}), 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=6, value=f"=ROUND(AVERAGE(Normalized!N{r_idx}:Q{r_idx}), 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=7, value=f"=ROUND(AVERAGE(Normalized!R{r_idx}:W{r_idx}), 2)").number_format = '0.00'
    
    # Baseline Opportunity Index: 25% each
    ws_index.cell(row=r_idx, column=8, value=f"=ROUND(0.25*D{r_idx} + 0.25*E{r_idx} + 0.25*F{r_idx} + 0.25*G{r_idx}, 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=8).font = font_bold
    ws_index.cell(row=r_idx, column=8).fill = fill_accent
    
    # Baseline Rank: =RANK(H2, H$2:H$37, 0)
    ws_index.cell(row=r_idx, column=9, value=f"=RANK(H{r_idx}, H$2:H${total_rows+1}, 0)").font = font_bold
    ws_index.cell(row=r_idx, column=9).alignment = Alignment(horizontal='center')
    
    # Scenario 1: Jobs Focus (40% Jobs, 20% others)
    ws_index.cell(row=r_idx, column=10, value=f"=ROUND(0.20*D{r_idx} + 0.20*E{r_idx} + 0.40*F{r_idx} + 0.20*G{r_idx}, 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=11, value=f"=RANK(J{r_idx}, J$2:J${total_rows+1}, 0)").alignment = Alignment(horizontal='center')
    
    # Scenario 2: School Focus (40% School, 20% others)
    ws_index.cell(row=r_idx, column=12, value=f"=ROUND(0.40*D{r_idx} + 0.20*E{r_idx} + 0.20*F{r_idx} + 0.20*G{r_idx}, 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=13, value=f"=RANK(L{r_idx}, L$2:L${total_rows+1}, 0)").alignment = Alignment(horizontal='center')
    
    # Scenario 3: Gender Focus (40% Gender, 20% others)
    ws_index.cell(row=r_idx, column=14, value=f"=ROUND(0.20*D{r_idx} + 0.20*E{r_idx} + 0.20*F{r_idx} + 0.40*G{r_idx}, 2)").number_format = '0.00'
    ws_index.cell(row=r_idx, column=15, value=f"=RANK(N{r_idx}, N$2:N${total_rows+1}, 0)").alignment = Alignment(horizontal='center')

    for c in range(1, 16):
        ws_index.cell(row=r_idx, column=c).border = border_thin

col_widths_index = [12, 32, 16, 18, 20, 16, 18, 20, 16, 18, 16, 18, 16, 18, 16]
for idx, w in enumerate(col_widths_index, 1):
    ws_index.column_dimensions[get_column_letter(idx)].width = w

# Save Workbook
wb.save('Opportunity_Lottery.xlsx')
print("Opportunity_Lottery.xlsx created successfully with live Excel formulas!")

