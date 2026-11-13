import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1: Overview & Methodology
c1 = nbf.v4.new_markdown_cell("""# Notebook 02: Index Building, Normalization & Sensitivity Analysis
## The Opportunity Lottery: Measuring Opportunity Disparities Across Indian States

### 1. Mathematical Formulation

#### A. Min-Max Normalization (0–100 Scale)
To synthesize diverse metrics (percentages, ratios, counts) onto a common scale:
- For **Higher is Better** indicators:
  $$S = \\frac{X - X_{\\min}}{X_{\\max} - X_{\\min}} \\times 100$$
- For **Lower is Better** indicators (e.g. dropout rates, unemployment, pupil-teacher ratios):
  $$S_{\\text{inverted}} = 100 - S = \\frac{X_{\\max} - X}{X_{\\max} - X_{\\min}} \\times 100$$

#### B. Thematic Sub-Indices
Each sub-index is the arithmetic mean of its constituent normalized indicators:
1. **School Access & Quality Sub-Index** (6 indicators: PTR, Dropout, Transition, Electricity, Girls' Toilets, Computers)
2. **Higher-Education Access Sub-Index** (4 indicators: GER Total, College Density, Average College Enrolment, Higher-Ed PTR)
3. **Jobs & Economy Sub-Index** (4 indicators: Youth Unemployment 15–29, Overall Unemployment, Youth LFPR, Regular Salaried Share)
4. **Gender Equality Sub-Index** (6 indicators: Higher-Ed GPI, Female LFPR 15+, Female Literacy, Literacy Gap, Female Youth Unemployment, Secondary Dropout Gap)

#### C. Composite Opportunity Index
The core baseline index is the equal-weighted arithmetic mean:
$$\\text{Opportunity Index} = 0.25 \\times \\text{School} + 0.25 \\times \\text{HigherEd} + 0.25 \\times \\text{Jobs} + 0.25 \\times \\text{Gender}$$

#### D. Sensitivity Stress-Testing (3 Scenarios)
- **Scenario 1 (Jobs Focus)**: 40% Jobs, 20% School, 20% Higher Ed, 20% Gender
- **Scenario 2 (School Focus)**: 40% School, 20% Higher Ed, 20% Jobs, 20% Gender
- **Scenario 3 (Gender Focus)**: 40% Gender, 20% School, 20% Higher Ed, 20% Jobs
""")

# Cell 2: Imports & Data Load
c2 = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load merged state master
df = pd.read_csv('../clean_data/state_master.csv')
print(f'Loaded state_master.csv: {df.shape[0]} states/UTs and {df.shape[1]} raw variables.')
df.head(3)
""")

# Cell 3: Normalization Config
c3 = nbf.v4.new_code_cell("""indicators_config = [
    # School Access & Quality
    {'col': 'ptr_secondary', 'theme': 'school', 'direction': 'lower_is_better'},
    {'col': 'dropout_sec_total', 'theme': 'school', 'direction': 'lower_is_better'},
    {'col': 'transition_rate_upprim_to_sec', 'theme': 'school', 'direction': 'higher_is_better'},
    {'col': 'pct_schools_electricity', 'theme': 'school', 'direction': 'higher_is_better'},
    {'col': 'pct_schools_girls_toilet', 'theme': 'school', 'direction': 'higher_is_better'},
    {'col': 'pct_schools_computers', 'theme': 'school', 'direction': 'higher_is_better'},
    
    # Higher-Education Access
    {'col': 'ger_higher_ed_total', 'theme': 'higher_ed', 'direction': 'higher_is_better'},
    {'col': 'colleges_per_lakh_pop', 'theme': 'higher_ed', 'direction': 'higher_is_better'},
    {'col': 'avg_enrolment_per_college', 'theme': 'higher_ed', 'direction': 'higher_is_better'},
    {'col': 'ptr_higher_ed', 'theme': 'higher_ed', 'direction': 'lower_is_better'},
    
    # Jobs & Economy
    {'col': 'youth_unemployment_rate_15_29', 'theme': 'jobs', 'direction': 'lower_is_better'},
    {'col': 'overall_unemployment_rate', 'theme': 'jobs', 'direction': 'lower_is_better'},
    {'col': 'youth_lfpr_15_29', 'theme': 'jobs', 'direction': 'higher_is_better'},
    {'col': 'regular_wage_salaried_share', 'theme': 'jobs', 'direction': 'higher_is_better'},
    
    # Gender Equality
    {'col': 'gpi_higher_ed', 'theme': 'gender', 'direction': 'higher_is_better'},
    {'col': 'female_lfpr_15_plus', 'theme': 'gender', 'direction': 'higher_is_better'},
    {'col': 'female_literacy_rate_plfs', 'theme': 'gender', 'direction': 'higher_is_better'},
    {'col': 'literacy_gender_gap_plfs', 'theme': 'gender', 'direction': 'lower_is_better'},
    {'col': 'youth_female_unemployment_rate', 'theme': 'gender', 'direction': 'lower_is_better'},
    {'col': 'dropout_sec_gender_gap', 'theme': 'gender', 'direction': 'lower_is_better'}
]

print(f'Total configured indicators: {len(indicators_config)}')
""")

# Cell 4: Compute Normalized Values
c4 = nbf.v4.new_code_cell("""df_norm = pd.DataFrame()
df_norm['state_code'] = df['state_code']
df_norm['state_name'] = df['state_name']
df_norm['entity_type'] = df['entity_type']

for item in indicators_config:
    col = item['col']
    vals = df[col]
    min_v, max_v = vals.min(), vals.max()
    
    if max_v != min_v:
        scaled = (vals - min_v) / (max_v - min_v) * 100
    else:
        scaled = vals * 0 + 50.0
        
    if item['direction'] == 'lower_is_better':
        scaled = 100.0 - scaled
        
    df_norm[f'norm_{col}'] = round(scaled, 2)

print('Normalization complete. Normalized DataFrame shape:', df_norm.shape)
df_norm.head(3)
""")

# Cell 5: Calculate Sub-Indices & Opportunity Index
c5 = nbf.v4.new_code_cell("""school_cols = [f\"norm_{i['col']}\" for i in indicators_config if i['theme'] == 'school']
higher_ed_cols = [f\"norm_{i['col']}\" for i in indicators_config if i['theme'] == 'higher_ed']
jobs_cols = [f\"norm_{i['col']}\" for i in indicators_config if i['theme'] == 'jobs']
gender_cols = [f\"norm_{i['col']}\" for i in indicators_config if i['theme'] == 'gender']

df_norm['subindex_school'] = round(df_norm[school_cols].mean(axis=1), 2)
df_norm['subindex_higher_ed'] = round(df_norm[higher_ed_cols].mean(axis=1), 2)
df_norm['subindex_jobs'] = round(df_norm[jobs_cols].mean(axis=1), 2)
df_norm['subindex_gender'] = round(df_norm[gender_cols].mean(axis=1), 2)

# Baseline Equal-Weighted Opportunity Index (25% each)
df_norm['opportunity_index'] = round(
    0.25 * df_norm['subindex_school'] +
    0.25 * df_norm['subindex_higher_ed'] +
    0.25 * df_norm['subindex_jobs'] +
    0.25 * df_norm['subindex_gender'],
    2
)

# Baseline Rank (1 = Highest Opportunity)
df_norm = df_norm.sort_values(by='opportunity_index', ascending=False).reset_index(drop=True)
df_norm['rank_baseline'] = df_norm.index + 1

print('Top 5 States in Baseline Opportunity Index:')
df_norm[['rank_baseline', 'state_name', 'subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 'opportunity_index']].head(5)
""")

# Cell 6: Sensitivity Testing
c6 = nbf.v4.new_code_cell("""# Scenario 1: Jobs Prioritized (40% Jobs, 20% School, 20% Higher Ed, 20% Gender)
df_norm['index_jobs_focus'] = round(0.20 * df_norm['subindex_school'] + 0.20 * df_norm['subindex_higher_ed'] + 0.40 * df_norm['subindex_jobs'] + 0.20 * df_norm['subindex_gender'], 2)
df_norm['rank_jobs_focus'] = df_norm['index_jobs_focus'].rank(ascending=False, method='min').astype(int)
df_norm['rank_shift_jobs'] = df_norm['rank_baseline'] - df_norm['rank_jobs_focus']

# Scenario 2: School Prioritized (40% School, 20% Higher Ed, 20% Jobs, 20% Gender)
df_norm['index_school_focus'] = round(0.40 * df_norm['subindex_school'] + 0.20 * df_norm['subindex_higher_ed'] + 0.20 * df_norm['subindex_jobs'] + 0.20 * df_norm['subindex_gender'], 2)
df_norm['rank_school_focus'] = df_norm['index_school_focus'].rank(ascending=False, method='min').astype(int)
df_norm['rank_shift_school'] = df_norm['rank_baseline'] - df_norm['rank_school_focus']

# Scenario 3: Gender Prioritized (40% Gender, 20% School, 20% Higher Ed, 20% Jobs)
df_norm['index_gender_focus'] = round(0.20 * df_norm['subindex_school'] + 0.20 * df_norm['subindex_higher_ed'] + 0.20 * df_norm['subindex_jobs'] + 0.40 * df_norm['subindex_gender'], 2)
df_norm['rank_gender_focus'] = df_norm['index_gender_focus'].rank(ascending=False, method='min').astype(int)
df_norm['rank_shift_gender'] = df_norm['rank_baseline'] - df_norm['rank_gender_focus']

# Spearman Rank Correlation with Baseline
rho_jobs, _ = stats.spearmanr(df_norm['rank_baseline'], df_norm['rank_jobs_focus'])
rho_school, _ = stats.spearmanr(df_norm['rank_baseline'], df_norm['rank_school_focus'])
rho_gender, _ = stats.spearmanr(df_norm['rank_baseline'], df_norm['rank_gender_focus'])

print(f'Spearman Rank Correlation (Baseline vs Jobs Focus): {rho_jobs:.4f}')
print(f'Spearman Rank Correlation (Baseline vs School Focus): {rho_school:.4f}')
print(f'Spearman Rank Correlation (Baseline vs Gender Focus): {rho_gender:.4f}')
""")

# Cell 7: Save clean opportunity_index.csv
c7 = nbf.v4.new_code_cell("""# Save opportunity_index.csv
df_norm.to_csv('../clean_data/opportunity_index.csv', index=False)
print('clean_data/opportunity_index.csv successfully written!')
""")

# Cell 8: Sensitivity Inspection Table
c8 = nbf.v4.new_code_cell("""preview_cols = [
    'rank_baseline', 'state_name', 'opportunity_index',
    'rank_jobs_focus', 'rank_shift_jobs',
    'rank_school_focus', 'rank_shift_school',
    'rank_gender_focus', 'rank_shift_gender'
]
print('=== TOP 10 STATES SENSITIVITY TABLE ===')
df_norm[preview_cols].head(10)
""")

nb.cells = [c1, c2, c3, c4, c5, c6, c7, c8]

with open('notebooks/02_index_building.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print('notebooks/02_index_building.ipynb created successfully!')

