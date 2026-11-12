"""
The Opportunity Lottery - Index Building & Sensitivity Stress-Testing Engine
Calculates:
1. Min-Max (0-100) Normalization with Inversion for 'lower is better' indicators
2. Four Sub-indices (School Quality, Higher-Ed Access, Jobs & Economy, Gender Equality)
3. Composite Opportunity Index (Equal-Weighted Baseline)
4. Three Alternative Weighting Scenarios for Sensitivity Testing
5. State Rankings & Rank Shifts
Outputs: clean_data/opportunity_index.csv
"""

import pandas as pd
import numpy as np

# Load merged state master
df = pd.read_csv('clean_data/state_master.csv')

# Define Indicators, Themes, and Directions
indicators_config = [
    # Theme 1: School Access & Quality
    {'col': 'ptr_secondary', 'theme': 'school', 'direction': 'lower_is_better'},
    {'col': 'dropout_sec_total', 'theme': 'school', 'direction': 'lower_is_better'},
    {'col': 'transition_rate_upprim_to_sec', 'theme': 'school', 'direction': 'higher_is_better'},
    {'col': 'pct_schools_electricity', 'theme': 'school', 'direction': 'higher_is_better'},
    {'col': 'pct_schools_girls_toilet', 'theme': 'school', 'direction': 'higher_is_better'},
    {'col': 'pct_schools_computers', 'theme': 'school', 'direction': 'higher_is_better'},
    
    # Theme 2: Higher-Education Access
    {'col': 'ger_higher_ed_total', 'theme': 'higher_ed', 'direction': 'higher_is_better'},
    {'col': 'colleges_per_lakh_pop', 'theme': 'higher_ed', 'direction': 'higher_is_better'},
    {'col': 'avg_enrolment_per_college', 'theme': 'higher_ed', 'direction': 'higher_is_better'},
    {'col': 'ptr_higher_ed', 'theme': 'higher_ed', 'direction': 'lower_is_better'},
    
    # Theme 3: Jobs & Economy
    {'col': 'youth_unemployment_rate_15_29', 'theme': 'jobs', 'direction': 'lower_is_better'},
    {'col': 'overall_unemployment_rate', 'theme': 'jobs', 'direction': 'lower_is_better'},
    {'col': 'youth_lfpr_15_29', 'theme': 'jobs', 'direction': 'higher_is_better'},
    {'col': 'regular_wage_salaried_share', 'theme': 'jobs', 'direction': 'higher_is_better'},
    
    # Theme 4: Gender Equality
    {'col': 'gpi_higher_ed', 'theme': 'gender', 'direction': 'higher_is_better'},
    {'col': 'female_lfpr_15_plus', 'theme': 'gender', 'direction': 'higher_is_better'},
    {'col': 'female_literacy_rate_plfs', 'theme': 'gender', 'direction': 'higher_is_better'},
    {'col': 'literacy_gender_gap_plfs', 'theme': 'gender', 'direction': 'lower_is_better'},
    {'col': 'youth_female_unemployment_rate', 'theme': 'gender', 'direction': 'lower_is_better'},
    {'col': 'dropout_sec_gender_gap', 'theme': 'gender', 'direction': 'lower_is_better'}
]

# Normalization Function
df_norm = pd.DataFrame()
df_norm['state_code'] = df['state_code']
df_norm['state_name'] = df['state_name']
df_norm['entity_type'] = df['entity_type']

for item in indicators_config:
    col = item['col']
    vals = df[col]
    min_v = vals.min()
    max_v = vals.max()
    
    # Min-max scale 0 to 100
    if max_v != min_v:
        scaled = (vals - min_v) / (max_v - min_v) * 100
    else:
        scaled = vals * 0 + 50.0
        
    if item['direction'] == 'lower_is_better':
        scaled = 100.0 - scaled
        
    df_norm[f'norm_{col}'] = round(scaled, 2)

# Calculate 4 Thematic Sub-Indices (Equal-weighted mean of normalized indicators)
school_cols = [f"norm_{i['col']}" for i in indicators_config if i['theme'] == 'school']
higher_ed_cols = [f"norm_{i['col']}" for i in indicators_config if i['theme'] == 'higher_ed']
jobs_cols = [f"norm_{i['col']}" for i in indicators_config if i['theme'] == 'jobs']
gender_cols = [f"norm_{i['col']}" for i in indicators_config if i['theme'] == 'gender']

df_norm['subindex_school'] = round(df_norm[school_cols].mean(axis=1), 2)
df_norm['subindex_higher_ed'] = round(df_norm[higher_ed_cols].mean(axis=1), 2)
df_norm['subindex_jobs'] = round(df_norm[jobs_cols].mean(axis=1), 2)
df_norm['subindex_gender'] = round(df_norm[gender_cols].mean(axis=1), 2)

# Composite Opportunity Index (Equal-weighted baseline: 25% each)
df_norm['opportunity_index'] = round(
    0.25 * df_norm['subindex_school'] +
    0.25 * df_norm['subindex_higher_ed'] +
    0.25 * df_norm['subindex_jobs'] +
    0.25 * df_norm['subindex_gender'],
    2
)

# Baseline Rank (1 = Highest Opportunity)
df_norm['rank_baseline'] = df_norm['opportunity_index'].rank(ascending=False, method='min').astype(int)

# Sensitivity Testing: 3 Alternative Weighting Scenarios
# Scenario 1: Jobs Prioritized (40% Jobs, 20% School, 20% Higher Ed, 20% Gender)
df_norm['index_jobs_focus'] = round(
    0.20 * df_norm['subindex_school'] +
    0.20 * df_norm['subindex_higher_ed'] +
    0.40 * df_norm['subindex_jobs'] +
    0.20 * df_norm['subindex_gender'],
    2
)
df_norm['rank_jobs_focus'] = df_norm['index_jobs_focus'].rank(ascending=False, method='min').astype(int)
df_norm['rank_shift_jobs'] = df_norm['rank_baseline'] - df_norm['rank_jobs_focus']

# Scenario 2: School Quality Prioritized (40% School, 20% Higher Ed, 20% Jobs, 20% Gender)
df_norm['index_school_focus'] = round(
    0.40 * df_norm['subindex_school'] +
    0.20 * df_norm['subindex_higher_ed'] +
    0.20 * df_norm['subindex_jobs'] +
    0.20 * df_norm['subindex_gender'],
    2
)
df_norm['rank_school_focus'] = df_norm['index_school_focus'].rank(ascending=False, method='min').astype(int)
df_norm['rank_shift_school'] = df_norm['rank_baseline'] - df_norm['rank_school_focus']

# Scenario 3: Gender Parity Prioritized (40% Gender, 20% School, 20% Higher Ed, 20% Jobs)
df_norm['index_gender_focus'] = round(
    0.20 * df_norm['subindex_school'] +
    0.20 * df_norm['subindex_higher_ed'] +
    0.20 * df_norm['subindex_jobs'] +
    0.40 * df_norm['subindex_gender'],
    2
)
df_norm['rank_gender_focus'] = df_norm['index_gender_focus'].rank(ascending=False, method='min').astype(int)
df_norm['rank_shift_gender'] = df_norm['rank_baseline'] - df_norm['rank_gender_focus']

# Sort by baseline opportunity index descending
df_norm = df_norm.sort_values(by='opportunity_index', ascending=False).reset_index(drop=True)
df_norm['rank_baseline'] = df_norm.index + 1

# Save clean opportunity index dataset
df_norm.to_csv('clean_data/opportunity_index.csv', index=False)
print("Opportunity Index Built Successfully!")
print(f"Shape: {df_norm.shape}")
print("\nTop 5 States by Opportunity Index:")
print(df_norm[['rank_baseline', 'state_name', 'subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 'opportunity_index']].head(5))

print("\nBottom 5 States by Opportunity Index:")
print(df_norm[['rank_baseline', 'state_name', 'subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 'opportunity_index']].tail(5))
