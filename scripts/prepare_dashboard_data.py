"""
Prepare Dashboard Data for Power BI and Opportunity Atlas
Creates dashboard/opportunity_powerbi_data.csv with 36 rows and rich attributes.
"""

import pandas as pd

df_idx = pd.read_csv('clean_data/opportunity_index.csv')
df_mast = pd.read_csv('clean_data/state_master.csv')
df_clust = pd.read_csv('clean_data/state_clusters.csv')

# Base columns
df = df_idx[['state_code', 'state_name', 'entity_type', 
             'subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 
             'opportunity_index', 'rank_baseline']].copy()

df.rename(columns={'rank_baseline': 'rank_all_36'}, inplace=True)

# Add rank for 28 states only
df_states = df[df['entity_type'] == 'State'].sort_values(by='opportunity_index', ascending=False).reset_index(drop=True)
df_states['rank_states_28'] = df_states.index + 1
df = df.merge(df_states[['state_name', 'rank_states_28']], on='state_name', how='left')

# Merge cluster info
df = df.merge(df_clust[['state_name', 'tier_code', 'opportunity_tier']], on='state_name')
df.rename(columns={'tier_code': 'cluster_code', 'opportunity_tier': 'cluster_profile'}, inplace=True)

# Add Region mapping
region_map = {
    'Jammu and Kashmir': 'North', 'Ladakh': 'North', 'Himachal Pradesh': 'North', 
    'Punjab': 'North', 'Uttarakhand': 'North', 'Haryana': 'North', 'Delhi': 'North', 
    'Chandigarh': 'North', 'Uttar Pradesh': 'North', 'Rajasthan': 'North',
    'Andhra Pradesh': 'South', 'Karnataka': 'South', 'Kerala': 'South', 
    'Tamil Nadu': 'South', 'Telangana': 'South', 'Puducherry': 'South', 'Lakshadweep': 'South',
    'Bihar': 'East', 'Jharkhand': 'East', 'Odisha': 'East', 'West Bengal': 'East', 'Andaman and Nicobar Islands': 'East',
    'Gujarat': 'West', 'Maharashtra': 'West', 'Goa': 'West', 'Dadra and Nagar Haveli and Daman and Diu': 'West',
    'Madhya Pradesh': 'Central', 'Chhattisgarh': 'Central',
    'Assam': 'North-East', 'Sikkim': 'North-East', 'Arunachal Pradesh': 'North-East', 
    'Nagaland': 'North-East', 'Manipur': 'North-East', 'Mizoram': 'North-East', 
    'Tripura': 'North-East', 'Meghalaya': 'North-East'
}
df['region'] = df['state_name'].map(region_map)

# Add key raw indicators from state_master
raw_cols = [
    'transition_rate_upprim_to_sec', 'dropout_sec_total', 'dropout_sec_boys', 'dropout_sec_girls',
    'pct_schools_electricity', 'ger_higher_ed_total', 'ger_higher_ed_male', 'ger_higher_ed_female',
    'gpi_higher_ed', 'colleges_per_lakh_pop', 'ptr_higher_ed', 'youth_unemployment_rate_15_29',
    'youth_female_unemployment_rate', 'female_lfpr_15_plus', 'regular_wage_salaried_share',
    'female_literacy_rate_plfs', 'male_literacy_rate_plfs', 'urban_population_pct_2011'
]
df = df.merge(df_mast[['state_name'] + raw_cols], on='state_name')

# Derived columns for visual convenience
df['retention_sec_boys'] = round(100 - df['dropout_sec_boys'], 2)
df['retention_sec_girls'] = round(100 - df['dropout_sec_girls'], 2)
df['retention_sec_total'] = round(100 - df['dropout_sec_total'], 2)

df.to_csv('dashboard/opportunity_powerbi_data.csv', index=False)
print("Dashboard export created successfully at dashboard/opportunity_powerbi_data.csv!")
print(f"Shape: {df.shape}")
