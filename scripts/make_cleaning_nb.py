import nbformat as nbf

nb = nbf.v4.new_notebook()

# 1. Header
cell1 = nbf.v4.new_markdown_cell("""# Notebook 01: Data Extraction, Cleaning & Harmonization
## The Opportunity Lottery: Indian States Opportunity Index

**Objective**: 
Extract, parse, standardize, and harmonize state-level indicators across 4 official Government of India sources:
1. **UDISE+ 2024–25**: School Infrastructure, Pupil-Teacher Ratio, Dropout & Transition Rates
2. **AISHE 2023–24**: Tertiary Gross Enrolment Ratio (GER), Gender Parity Index (GPI), College Density, Pupil-Teacher Ratio
3. **PLFS 2025 (Calendar Year)**: Youth Unemployment (15–29), Labour Force Participation, Regular Salaried Worker Share, Modern Literacy
4. **Census of India 2011**: Baseline Demographics, Population Base, Urbanization Share

Outputs clean standardized files in `clean_data/` and merges them into `clean_data/state_master.csv` (36 States & UTs).
""")

# 2. Imports
cell2 = nbf.v4.new_code_cell("""import os
import re
import pdfplumber
import openpyxl
import pandas as pd
import numpy as np

# Load canonical 36 master state list
master_df = pd.read_csv('../clean_data/master_state_list.csv')
print(f'Master state list loaded: {len(master_df)} States & UTs.')
master_df.head(5)
""")

# 3. State Matcher
cell3 = nbf.v4.new_code_cell("""state_names = master_df['state_name'].tolist()

def match_state_name(raw):
    \"\"\"Robustly maps raw state name strings to canonical 36 master state names.\"\"\"
    if not isinstance(raw, str):
        return None
    raw_clean = raw.strip()
    raw_lower = raw_clean.lower().replace('.', '').replace('&', 'and')
    
    for s in state_names:
        s_clean = s.lower().replace('&', 'and')
        if s_clean == raw_lower:
            return s
            
    if 'andaman' in raw_lower:
        return 'Andaman and Nicobar Islands'
    if 'dadra' in raw_lower or 'daman' in raw_lower or 'dnh' in raw_lower:
        return 'Dadra and Nagar Haveli and Daman and Diu'
    if 'jammu' in raw_lower or 'kashmir' in raw_lower:
        return 'Jammu and Kashmir'
    if 'ladakh' in raw_lower:
        return 'Ladakh'
    if 'delhi' in raw_lower:
        return 'Delhi'
    if 'puducherry' in raw_lower or 'pondicherry' in raw_lower:
        return 'Puducherry'
    if 'telangana' in raw_lower or 'telengana' in raw_lower:
        return 'Telangana'
    if 'odisha' in raw_lower or 'orissa' in raw_lower:
        return 'Odisha'
    if 'uttarakhand' in raw_lower or 'uttaranchal' in raw_lower:
        return 'Uttarakhand'
    if 'chhattisgarh' in raw_lower or 'chhatisgarh' in raw_lower:
        return 'Chhattisgarh'
        
    for idx, row in master_df.iterrows():
        alts = str(row['alternate_names']).split(';')
        for a in alts:
            a_clean = a.strip().lower().replace('&', 'and')
            if a_clean == raw_lower or a_clean in raw_lower or raw_lower in a_clean:
                return row['state_name']
    return None

def normalize_pdf_lines(lines):
    \"\"\"Handles multi-line broken entity names (e.g. Dadra and Nagar Haveli wrapping).\"\"\"
    cleaned = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ('Dadra' in line or 'Daman' in line) and not any(c.isdigit() for c in line) and i + 1 < len(lines):
            next_l = lines[i+1].strip()
            if any(c.isdigit() for c in next_l):
                if i + 2 < len(lines) and ('Daman' in lines[i+2] or 'DNH' in lines[i+2]):
                    cleaned.append(f'Dadra and Nagar Haveli and Daman and Diu {next_l}')
                    i += 3
                    continue
                else:
                    cleaned.append(f'Dadra and Nagar Haveli and Daman and Diu {next_l}')
                    i += 2
                    continue
            elif 'Daman' in next_l:
                if i + 2 < len(lines) and any(c.isdigit() for c in lines[i+2]):
                    cleaned.append(f'Dadra and Nagar Haveli and Daman and Diu {lines[i+2].strip()}')
                    i += 3
                    continue
        cleaned.append(line)
        i += 1
    return cleaned
""")

# 4. AISHE
cell4 = nbf.v4.new_code_cell("""# Extraction 1: AISHE 2023-24
aishe_path = '../raw_data/AISHE Final Report 2023-24.xlsx'

# 1. GER
df_ger = pd.read_excel(aishe_path, sheet_name='19GER(2011)')
ger_records = []
for idx in range(3, len(df_ger)):
    row = df_ger.iloc[idx]
    st = match_state_name(str(row.iloc[1]))
    if st and st != 'India':
        ger_records.append({
            'state_name': st,
            'ger_higher_ed_male': round(float(row.iloc[2]), 2) if pd.notna(row.iloc[2]) else np.nan,
            'ger_higher_ed_female': round(float(row.iloc[3]), 2) if pd.notna(row.iloc[3]) else np.nan,
            'ger_higher_ed_total': round(float(row.iloc[4]), 2) if pd.notna(row.iloc[4]) else np.nan
        })
df_ger_clean = pd.DataFrame(ger_records).drop_duplicates(subset=['state_name'])

# 2. GPI
df_gpi = pd.read_excel(aishe_path, sheet_name='20GPI2011')
gpi_records = []
for idx in range(2, len(df_gpi)):
    row = df_gpi.iloc[idx]
    st = match_state_name(str(row.iloc[1]))
    if st and st != 'India':
        gpi_records.append({
            'state_name': st,
            'gpi_higher_ed': round(float(row.iloc[2]), 2) if pd.notna(row.iloc[2]) else np.nan
        })
df_gpi_clean = pd.DataFrame(gpi_records).drop_duplicates(subset=['state_name'])

# 3. College Density & Enrolment
df_col = pd.read_excel(aishe_path, sheet_name='4CollegeIndicator')
col_records = []
for idx in range(3, len(df_col)):
    row = df_col.iloc[idx]
    st = match_state_name(str(row.iloc[1]))
    if st and st != 'India':
        col_records.append({
            'state_name': st,
            'colleges_per_lakh_pop': round(float(row.iloc[3]), 2) if pd.notna(row.iloc[3]) else np.nan,
            'avg_enrolment_per_college': round(float(row.iloc[5]), 1) if pd.notna(row.iloc[5]) else np.nan
        })
df_col_clean = pd.DataFrame(col_records).drop_duplicates(subset=['state_name'])

# 4. PTR Higher Ed
df_ptr = pd.read_excel(aishe_path, sheet_name='25PTR')
ptr_records = []
for idx in range(3, len(df_ptr)):
    row = df_ptr.iloc[idx]
    st = match_state_name(str(row.iloc[1]))
    if st and st != 'India':
        ptr_records.append({
            'state_name': st,
            'ptr_higher_ed': round(float(row.iloc[5]), 1) if pd.notna(row.iloc[5]) else np.nan
        })
df_ptr_clean = pd.DataFrame(ptr_records).drop_duplicates(subset=['state_name'])

df_aishe = master_df[['state_code', 'state_name']].merge(df_ger_clean, on='state_name', how='left')
df_aishe = df_aishe.merge(df_gpi_clean, on='state_name', how='left')
df_aishe = df_aishe.merge(df_col_clean, on='state_name', how='left')
df_aishe = df_aishe.merge(df_ptr_clean, on='state_name', how='left')
df_aishe['aishe_year'] = '2023-24'
df_aishe.to_csv('../clean_data/aishe_clean.csv', index=False)
print('AISHE Cleaned:', df_aishe.shape)
df_aishe.head(3)
""")

# 5. UDISE+
cell5 = nbf.v4.new_code_cell("""# Extraction 2: UDISE+ 2024-25
udise_path = '../raw_data/UDISE+2024_25_Booklet_existing.118ba29d4773e6372f72.pdf'

with pdfplumber.open(udise_path) as pdf:
    # 1. PTR Secondary (Page 63)
    p63_lines = normalize_pdf_lines(pdf.pages[62].extract_text().split('\\n'))
    udise_ptr = {}
    for l in p63_lines:
        toks = l.split()
        if len(toks) >= 5:
            try:
                nums = [float(t) for t in toks[-4:]]
                name_p = ' '.join(toks[:-4])
                st = match_state_name(name_p)
                if st:
                    udise_ptr[st] = nums[2]
            except ValueError:
                pass
                
    # 2. Dropout Secondary (Page 120)
    p120_lines = normalize_pdf_lines(pdf.pages[119].extract_text().split('\\n'))
    udise_drop = {}
    for l in p120_lines:
        toks = l.split()
        if len(toks) >= 10:
            try:
                nums = [float(t) for t in toks[-9:]]
                name_p = ' '.join(toks[:-9])
                st = match_state_name(name_p)
                if st:
                    udise_drop[st] = {
                        'dropout_sec_boys': nums[6],
                        'dropout_sec_girls': nums[7],
                        'dropout_sec_total': nums[8],
                        'dropout_sec_gender_gap': round(nums[7] - nums[6], 2)
                    }
            except ValueError:
                pass

    # 3. Transition Rate Upper Primary to Secondary (Page 121)
    p121_lines = normalize_pdf_lines(pdf.pages[120].extract_text().split('\\n'))
    udise_trans = {}
    for l in p121_lines:
        toks = l.split()
        if len(toks) >= 10:
            try:
                nums = [float(t) for t in toks[-9:]]
                name_p = ' '.join(toks[:-9])
                st = match_state_name(name_p)
                if st:
                    udise_trans[st] = nums[5]
            except ValueError:
                pass

    # 4. Functional Electricity (Page 161)
    p161_lines = normalize_pdf_lines(pdf.pages[160].extract_text().split('\\n'))
    udise_elec = {}
    for l in p161_lines:
        toks = l.split()
        if len(toks) >= 3:
            for idx, t in enumerate(toks):
                try:
                    val = float(t)
                    name_p = ' '.join(toks[:idx])
                    st = match_state_name(name_p)
                    if st and st not in udise_elec:
                        udise_elec[st] = val
                        break
                except ValueError:
                    pass

    # 5. Functional Girls Toilets (Page 163)
    p163_lines = normalize_pdf_lines(pdf.pages[162].extract_text().split('\\n'))
    udise_toilet = {}
    for l in p163_lines:
        toks = l.split()
        if len(toks) >= 3:
            for idx, t in enumerate(toks):
                try:
                    val = float(t)
                    name_p = ' '.join(toks[:idx])
                    st = match_state_name(name_p)
                    if st and st not in udise_toilet:
                        udise_toilet[st] = val
                        break
                except ValueError:
                    pass

    # 6. Functional Computers (Page 138)
    p138_lines = normalize_pdf_lines(pdf.pages[137].extract_text().split('\\n'))
    udise_comp = {}
    for l in p138_lines:
        toks = l.split()
        name_toks, num_toks = [], []
        for t in toks:
            try:
                num_toks.append(float(t.replace(',', '')))
            except ValueError:
                name_toks.append(t)
        name_p = ' '.join(name_toks)
        st = match_state_name(name_p)
        if st and len(num_toks) >= 10:
            udise_comp[st] = num_toks[-4] if len(num_toks) >= 14 else num_toks[-1]

    # 7. Internet Facility (Page 139)
    p139_lines = normalize_pdf_lines(pdf.pages[138].extract_text().split('\\n'))
    udise_net = {}
    for l in p139_lines:
        toks = l.split()
        name_toks, num_toks = [], []
        for t in toks:
            try:
                num_toks.append(float(t.replace(',', '')))
            except ValueError:
                name_toks.append(t)
        name_p = ' '.join(name_toks)
        st = match_state_name(name_p)
        if st and len(num_toks) >= 10:
            udise_net[st] = num_toks[-4] if len(num_toks) >= 14 else num_toks[-1]

udise_records = []
for st in state_names:
    drop_info = udise_drop.get(st, {})
    udise_records.append({
        'state_name': st,
        'ptr_secondary': udise_ptr.get(st, np.nan),
        'dropout_sec_total': drop_info.get('dropout_sec_total', np.nan),
        'dropout_sec_boys': drop_info.get('dropout_sec_boys', np.nan),
        'dropout_sec_girls': drop_info.get('dropout_sec_girls', np.nan),
        'dropout_sec_gender_gap': drop_info.get('dropout_sec_gender_gap', np.nan),
        'transition_rate_upprim_to_sec': udise_trans.get(st, np.nan),
        'pct_schools_electricity': udise_elec.get(st, np.nan),
        'pct_schools_girls_toilet': udise_toilet.get(st, np.nan),
        'pct_schools_computers': udise_comp.get(st, np.nan),
        'pct_schools_internet': udise_net.get(st, np.nan),
        'udise_year': '2024-25'
    })

df_udise = master_df[['state_code', 'state_name']].merge(pd.DataFrame(udise_records), on='state_name')
df_udise.to_csv('../clean_data/udise_clean.csv', index=False)
print('UDISE+ Cleaned:', df_udise.shape)
df_udise.head(3)
""")

# 6. PLFS
cell6 = nbf.v4.new_code_cell("""# Extraction 3: PLFS Calendar Year 2025
plfs_path = '../raw_data/Annual_Report_PLFS_2025.pdf'

with pdfplumber.open(plfs_path) as pdf:
    # 1. Youth Unemployment Rate (Page 152)
    p152_lines = [l.strip() for l in pdf.pages[151].extract_text().split('\\n') if l.strip()]
    plfs_ur_youth = {}
    for l in p152_lines:
        toks = l.split()
        if len(toks) >= 7:
            if 'Chandigarh' in l:
                try:
                    nums = [float(t) for t in toks[-3:]]
                    plfs_ur_youth['Chandigarh'] = {'youth_ur_male': nums[0], 'youth_ur_female': nums[1], 'youth_ur_total': nums[2]}
                except ValueError:
                    pass
            else:
                try:
                    nums = [float(t) for t in toks[-3:]]
                    name_p = ' '.join(toks[:-9]) if len(toks) >= 10 else ' '.join(toks[:-3])
                    st = match_state_name(name_p)
                    if st and st not in plfs_ur_youth:
                        plfs_ur_youth[st] = {'youth_ur_male': nums[0], 'youth_ur_female': nums[1], 'youth_ur_total': nums[2]}
                except ValueError:
                    pass

    # 2. Overall Unemployment Rate (Page 155)
    p155_lines = [l.strip() for l in pdf.pages[154].extract_text().split('\\n') if l.strip()]
    plfs_ur_overall = {}
    for l in p155_lines:
        toks = l.split()
        if len(toks) >= 7:
            if 'Chandigarh' in l:
                try:
                    plfs_ur_overall['Chandigarh'] = float(toks[-1])
                except ValueError:
                    pass
            else:
                try:
                    val = float(toks[-1])
                    name_p = ' '.join(toks[:-9]) if len(toks) >= 10 else ' '.join(toks[:-3])
                    st = match_state_name(name_p)
                    if st and st not in plfs_ur_overall:
                        plfs_ur_overall[st] = val
                except ValueError:
                    pass

    # 3. Youth LFPR (15-29 years, Page 142)
    p142_lines = [l.strip() for l in pdf.pages[141].extract_text().split('\\n') if l.strip()]
    plfs_lfpr_youth = {}
    for l in p142_lines:
        toks = l.split()
        if len(toks) >= 7:
            if 'Chandigarh' in l:
                try:
                    plfs_lfpr_youth['Chandigarh'] = float(toks[-1])
                except ValueError:
                    pass
            else:
                try:
                    val = float(toks[-1])
                    name_p = ' '.join(toks[:-9]) if len(toks) >= 10 else ' '.join(toks[:-3])
                    st = match_state_name(name_p)
                    if st and st not in plfs_lfpr_youth:
                        plfs_lfpr_youth[st] = val
                except ValueError:
                    pass

    # 4. Female LFPR (15+ years, Page 144)
    p144_lines = [l.strip() for l in pdf.pages[143].extract_text().split('\\n') if l.strip()]
    plfs_lfpr_female_15plus = {}
    for l in p144_lines:
        toks = l.split()
        if len(toks) >= 7:
            if 'Chandigarh' in l:
                try:
                    plfs_lfpr_female_15plus['Chandigarh'] = float(toks[-2])
                except ValueError:
                    pass
            else:
                try:
                    val = float(toks[-2])
                    name_p = ' '.join(toks[:-9]) if len(toks) >= 10 else ' '.join(toks[:-3])
                    st = match_state_name(name_p)
                    if st and st not in plfs_lfpr_female_15plus:
                        plfs_lfpr_female_15plus[st] = val
                except ValueError:
                    pass

    # 5. Regular Wage / Salaried Worker Share (Page 165)
    p165_lines = [l.strip() for l in pdf.pages[164].extract_text().split('\\n') if l.strip()]
    plfs_salaried = {}
    for l in p165_lines:
        toks = l.split()
        if len(toks) >= 7:
            try:
                reg_wage = float(toks[-3])
                name_p = ' '.join(toks[:-6])
                st = match_state_name(name_p)
                if st and st not in plfs_salaried:
                    plfs_salaried[st] = reg_wage
            except ValueError:
                pass

    # 6. Literacy Rates from PLFS Table 7 (Page 87: Rural+Urban, age 7 & above)
    p87_lines = [l.strip() for l in pdf.pages[86].extract_text().split('\\n') if l.strip()]
    plfs_lit = {}
    for l in p87_lines:
        toks = l.split()
        if len(toks) >= 7:
            try:
                m_lit = float(toks[-6])
                f_lit = float(toks[-4])
                p_lit = float(toks[-2])
                name_p = ' '.join(toks[:-6])
                st = match_state_name(name_p)
                if st and st not in plfs_lit:
                    plfs_lit[st] = {
                        'lit_male': m_lit,
                        'lit_female': f_lit,
                        'lit_total': p_lit
                    }
            except ValueError:
                pass

plfs_records = []
for st in state_names:
    ur_info = plfs_ur_youth.get(st, {})
    lit_info = plfs_lit.get(st, {})
    f_lit = lit_info.get('lit_female', np.nan)
    m_lit = lit_info.get('lit_male', np.nan)
    p_lit = lit_info.get('lit_total', np.nan)
    plfs_records.append({
        'state_name': st,
        'youth_unemployment_rate_15_29': ur_info.get('youth_ur_total', np.nan),
        'youth_female_unemployment_rate': ur_info.get('youth_ur_female', np.nan),
        'youth_male_unemployment_rate': ur_info.get('youth_ur_male', np.nan),
        'overall_unemployment_rate': plfs_ur_overall.get(st, np.nan),
        'youth_lfpr_15_29': plfs_lfpr_youth.get(st, np.nan),
        'female_lfpr_15_plus': plfs_lfpr_female_15plus.get(st, np.nan),
        'regular_wage_salaried_share': plfs_salaried.get(st, np.nan),
        'female_literacy_rate_plfs': f_lit,
        'male_literacy_rate_plfs': m_lit,
        'total_literacy_rate_plfs': p_lit,
        'literacy_gender_gap_plfs': round(m_lit - f_lit, 2) if pd.notna(m_lit) and pd.notna(f_lit) else np.nan,
        'plfs_year': '2025'
    })

df_plfs = master_df[['state_code', 'state_name']].merge(pd.DataFrame(plfs_records), on='state_name')
df_plfs.to_csv('../clean_data/plfs_clean.csv', index=False)
print('PLFS Cleaned:', df_plfs.shape)
df_plfs.head(3)
""")

# 7. Census 2011
cell7 = nbf.v4.new_code_cell("""# Extraction 4: Census 2011 Baseline with Harmonized Boundaries
census_path = '../raw_data/2011-IndiaState-0000.xlsx'
df_raw_census = pd.read_excel(census_path)

census_total = df_raw_census[df_raw_census['TRU'] == 'Total']
census_urban = df_raw_census[df_raw_census['TRU'] == 'Urban']

census_records = []
for idx, row in census_total.iterrows():
    raw_name = str(row['Name'])
    st = match_state_name(raw_name)
    if st and st != 'India':
        tot_p = float(row['TOT_P'])
        tot_m = float(row['TOT_M'])
        tot_f = float(row['TOT_F'])
        p_06 = float(row['P_06'])
        m_06 = float(row['M_06'])
        f_06 = float(row['F_06'])
        p_lit = float(row['P_LIT'])
        m_lit = float(row['M_LIT'])
        f_lit = float(row['F_LIT'])
        
        lit_total = round((p_lit / (tot_p - p_06)) * 100, 2) if (tot_p - p_06) > 0 else np.nan
        lit_male = round((m_lit / (tot_m - m_06)) * 100, 2) if (tot_m - m_06) > 0 else np.nan
        lit_female = round((f_lit / (tot_f - f_06)) * 100, 2) if (tot_f - f_06) > 0 else np.nan
        lit_gap = round(lit_male - lit_female, 2) if pd.notna(lit_male) and pd.notna(f_lit) else np.nan
        
        urban_row = census_urban[census_urban['State'] == row['State']]
        urban_p = float(urban_row['TOT_P'].values[0]) if len(urban_row) > 0 else 0.0
        urban_share = round((urban_p / tot_p) * 100, 2) if tot_p > 0 else np.nan
        
        census_records.append({
            'state_name': st,
            'population_2011': int(tot_p),
            'urban_population_pct_2011': urban_share,
            'literacy_rate_2011': lit_total,
            'female_literacy_rate_2011': lit_female,
            'literacy_gender_gap_2011': lit_gap
        })

df_census_parsed = pd.DataFrame(census_records)

# Merge DNH & DD
dnh_dd_entries = df_census_parsed[df_census_parsed['state_name'] == 'Dadra and Nagar Haveli and Daman and Diu']
if len(dnh_dd_entries) > 1:
    tot_pop = dnh_dd_entries['population_2011'].sum()
    w_urban = (dnh_dd_entries['population_2011'] * dnh_dd_entries['urban_population_pct_2011']).sum() / tot_pop
    w_lit = (dnh_dd_entries['population_2011'] * dnh_dd_entries['literacy_rate_2011']).sum() / tot_pop
    w_flit = (dnh_dd_entries['population_2011'] * dnh_dd_entries['female_literacy_rate_2011']).sum() / tot_pop
    w_gap = (dnh_dd_entries['population_2011'] * dnh_dd_entries['literacy_gender_gap_2011']).sum() / tot_pop
    
    df_census_parsed = df_census_parsed[df_census_parsed['state_name'] != 'Dadra and Nagar Haveli and Daman and Diu']
    merged_dnh_dd = pd.DataFrame([{
        'state_name': 'Dadra and Nagar Haveli and Daman and Diu',
        'population_2011': tot_pop,
        'urban_population_pct_2011': round(w_urban, 2),
        'literacy_rate_2011': round(w_lit, 2),
        'female_literacy_rate_2011': round(w_flit, 2),
        'literacy_gender_gap_2011': round(w_gap, 2)
    }])
    df_census_parsed = pd.concat([df_census_parsed, merged_dnh_dd], ignore_index=True)

# Reconcile bifurcated states from official Census 2011 district aggregations
bifurcated_census = [
    {'state_name': 'Telangana', 'population_2011': 35003674, 'urban_population_pct_2011': 38.67, 'literacy_rate_2011': 66.54, 'female_literacy_rate_2011': 57.99, 'literacy_gender_gap_2011': 17.10},
    {'state_name': 'Andhra Pradesh', 'population_2011': 49577103, 'urban_population_pct_2011': 29.47, 'literacy_rate_2011': 67.35, 'female_literacy_rate_2011': 59.96, 'literacy_gender_gap_2011': 14.83},
    {'state_name': 'Ladakh', 'population_2011': 274289, 'urban_population_pct_2011': 22.61, 'literacy_rate_2011': 77.48, 'female_literacy_rate_2011': 64.28, 'literacy_gender_gap_2011': 22.86},
    {'state_name': 'Jammu and Kashmir', 'population_2011': 12267013, 'urban_population_pct_2011': 27.38, 'literacy_rate_2011': 67.16, 'female_literacy_rate_2011': 56.43, 'literacy_gender_gap_2011': 20.35}
]

df_census_parsed = df_census_parsed[~df_census_parsed['state_name'].isin(['Andhra Pradesh', 'Jammu and Kashmir', 'Telangana', 'Ladakh'])]
df_census_parsed = pd.concat([df_census_parsed, pd.DataFrame(bifurcated_census)], ignore_index=True)

df_census = master_df[['state_code', 'state_name']].merge(df_census_parsed, on='state_name', how='left')
df_census['census_year'] = '2011'
df_census.to_csv('../clean_data/census_clean.csv', index=False)
print('Census Cleaned:', df_census.shape)
df_census.head(3)
""")

# 8. Merge into state_master.csv
cell8 = nbf.v4.new_code_cell("""# Merge all 4 clean datasets into state_master.csv
state_master = master_df[['state_code', 'state_name', 'entity_type']].copy()
state_master = state_master.merge(df_udise.drop(columns=['state_code']), on='state_name', how='left')
state_master = state_master.merge(df_aishe.drop(columns=['state_code']), on='state_name', how='left')
state_master = state_master.merge(df_plfs.drop(columns=['state_code']), on='state_name', how='left')
state_master = state_master.merge(df_census.drop(columns=['state_code']), on='state_name', how='left')

state_master.to_csv('../clean_data/state_master.csv', index=False)
print('State Master Created Successfully!')
print('Shape:', state_master.shape)
print('Null Count across all columns:')
nulls = state_master.isnull().sum()
if nulls.sum() == 0:
    print('SUCCESS: Zero missing values across all 36 States/UTs!')
else:
    print(nulls[nulls > 0])
""")

# 9. Preview
cell9 = nbf.v4.new_code_cell("""# Preview key indicators across states
cols_preview = [
    'state_name', 'ptr_secondary', 'dropout_sec_total', 'pct_schools_electricity',
    'ger_higher_ed_total', 'colleges_per_lakh_pop', 'youth_unemployment_rate_15_29',
    'female_lfpr_15_plus', 'female_literacy_rate_plfs'
]
state_master[cols_preview].sort_values(by='ger_higher_ed_total', ascending=False).head(10)
""")

nb.cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

with open('notebooks/01_cleaning.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print('notebooks/01_cleaning.ipynb created successfully!')

