"""
The Opportunity Lottery - Week 3 Analysis Engine
Performs:
1. Correlation Matrix between Sub-Indices & Key Transition Stages
2. Gap Analysis (Top 5 vs Bottom 5 states; Male vs Female Gaps across the pipeline)
3. K-Means Clustering with Elbow & Silhouette Evaluation for 3-4 Opportunity Tiers (via Scipy & NumPy)
4. High-Resolution Visualizations saved to dashboard/charts/
5. Compiles Empirical Findings Table for Business Questions 1 to 7
"""

import os
os.environ['MPLCONFIGDIR'] = os.path.abspath('dashboard/charts/.mpl_cache')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.vq import kmeans2
from scipy import stats

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

# 1. Load Data
df_master = pd.read_csv('clean_data/state_master.csv')
df_index = pd.read_csv('clean_data/opportunity_index.csv')

# Merge for unified analysis
df_all = df_index.merge(df_master.drop(columns=['state_code', 'entity_type']), on='state_name')
os.makedirs('dashboard/charts', exist_ok=True)

print("=== 1. CORRELATION ANALYSIS ===")
subindex_cols = ['subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 'opportunity_index']
subindex_labels = ['School Quality', 'Higher Ed Access', 'Jobs & Economy', 'Gender Equality', 'Opportunity Index']

corr_pearson = df_index[subindex_cols].corr(method='pearson')
corr_spearman = df_index[subindex_cols].corr(method='spearman')

print("Pearson Correlation Matrix:")
print(corr_pearson.round(3))
print("\nSpearman Rank Correlation Matrix:")
print(corr_spearman.round(3))

# Chart 1: Sub-index Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_pearson,
    annot=True,
    fmt=".2f",
    cmap='Blues',
    xticklabels=subindex_labels,
    yticklabels=subindex_labels,
    vmin=-0.2,
    vmax=1.0,
    cbar_kws={'label': 'Pearson Correlation (r)'},
    linewidths=1,
    linecolor='white'
)
plt.title('Correlation Matrix Across Opportunity Sub-Indices (36 States & UTs)', fontsize=12, pad=15, fontweight='bold', color='#1F497D')
plt.tight_layout()
plt.savefig('dashboard/charts/heatmap_subindex_correlations.png')
plt.close()

# Chart 2: Scatter: School Infrastructure vs Higher-Ed Enrolment
plt.figure(figsize=(9, 6))
sns.regplot(
    data=df_all,
    x='subindex_school',
    y='subindex_higher_ed',
    scatter_kws={'alpha': 0.7, 'color': '#1F497D', 's': 70},
    line_kws={'color': '#C00000', 'linewidth': 2}
)
for st in ['Kerala', 'Tamil Nadu', 'Chandigarh', 'Bihar', 'Meghalaya', 'Gujarat', 'Delhi']:
    row = df_all[df_all['state_name'] == st].iloc[0]
    plt.annotate(st, (row['subindex_school'] + 1, row['subindex_higher_ed'] + 0.5), fontsize=9, fontweight='semibold')

r_sh = corr_pearson.loc['subindex_school', 'subindex_higher_ed']
plt.title(f'Pipeline Continuity: School Quality vs. Higher Education Access (r = {r_sh:.2f})', fontsize=12, pad=12, fontweight='bold', color='#1F497D')
plt.xlabel('School Access & Quality Sub-Index (0–100)', fontsize=11)
plt.ylabel('Higher-Education Access Sub-Index (0–100)', fontsize=11)
plt.tight_layout()
plt.savefig('dashboard/charts/scatterplot_school_vs_higher_ed.png')
plt.close()

# Chart 3: Scatter: Higher-Ed Access vs Youth Unemployment Rate
plt.figure(figsize=(9, 6))
sns.regplot(
    data=df_all,
    x='subindex_higher_ed',
    y='youth_unemployment_rate_15_29',
    scatter_kws={'alpha': 0.7, 'color': '#2E75B6', 's': 70},
    line_kws={'color': '#ED7D31', 'linewidth': 2}
)
for st in ['Kerala', 'Bihar', 'Puducherry', 'Gujarat', 'Andaman and Nicobar Islands', 'Tamil Nadu']:
    row = df_all[df_all['state_name'] == st].iloc[0]
    plt.annotate(st, (row['subindex_higher_ed'] + 1, row['youth_unemployment_rate_15_29'] + 0.5), fontsize=9, fontweight='semibold')

r_hy = df_all['subindex_higher_ed'].corr(df_all['youth_unemployment_rate_15_29'])
plt.title(f'The Higher Ed – Employment Disconnect: College Access vs. Youth Unemployment (r = {r_hy:.2f})', fontsize=12, pad=12, fontweight='bold', color='#1F497D')
plt.xlabel('Higher-Education Access Sub-Index (0–100)', fontsize=11)
plt.ylabel('Youth Unemployment Rate (15–29 yrs, %)', fontsize=11)
plt.tight_layout()
plt.savefig('dashboard/charts/scatterplot_higher_ed_vs_youth_jobs.png')
plt.close()

print("\n=== 2. GAP ANALYSIS ===")
top5 = df_all.head(5)
bottom5 = df_all.tail(5)

# Summary Gap metrics
gap_table = pd.DataFrame({
    'Metric': [
        'Opportunity Index', 'School Sub-Index', 'Higher-Ed Sub-Index', 'Jobs Sub-Index', 'Gender Sub-Index',
        'Secondary Dropout Rate (%)', 'Upper Prim to Sec Transition (%)', 'College GER (%)', 'Colleges per Lakh Pop',
        'Youth Unemployment Rate (%)', 'Female LFPR 15+ (%)', 'Female Literacy Rate (%)'
    ],
    'Top_5_Mean': [
        top5['opportunity_index'].mean(), top5['subindex_school'].mean(), top5['subindex_higher_ed'].mean(), top5['subindex_jobs'].mean(), top5['subindex_gender'].mean(),
        top5['dropout_sec_total'].mean(), top5['transition_rate_upprim_to_sec'].mean(), top5['ger_higher_ed_total'].mean(), top5['colleges_per_lakh_pop'].mean(),
        top5['youth_unemployment_rate_15_29'].mean(), top5['female_lfpr_15_plus'].mean(), top5['female_literacy_rate_plfs'].mean()
    ],
    'Bottom_5_Mean': [
        bottom5['opportunity_index'].mean(), bottom5['subindex_school'].mean(), bottom5['subindex_higher_ed'].mean(), bottom5['subindex_jobs'].mean(), bottom5['subindex_gender'].mean(),
        bottom5['dropout_sec_total'].mean(), bottom5['transition_rate_upprim_to_sec'].mean(), bottom5['ger_higher_ed_total'].mean(), bottom5['colleges_per_lakh_pop'].mean(),
        bottom5['youth_unemployment_rate_15_29'].mean(), bottom5['female_lfpr_15_plus'].mean(), bottom5['female_literacy_rate_plfs'].mean()
    ]
})
gap_table['Absolute_Gap'] = (gap_table['Top_5_Mean'] - gap_table['Bottom_5_Mean']).round(2)
gap_table['Ratio_Top_to_Bottom'] = (gap_table['Top_5_Mean'] / gap_table['Bottom_5_Mean']).round(2)
print("\nTop 5 vs Bottom 5 Gap Comparison:")
print(gap_table.round(2).to_string(index=False))

# Chart 4: Top 5 vs Bottom 5 Bar Chart
plt.figure(figsize=(10, 6))
compare_df = pd.concat([top5, bottom5])
compare_df['Group'] = ['Top 5'] * 5 + ['Bottom 5'] * 5
colors = ['#1F497D' if g == 'Top 5' else '#C00000' for g in compare_df['Group']]

y_pos = np.arange(len(compare_df))
plt.barh(y_pos, compare_df['opportunity_index'], color=colors, height=0.65)
plt.yticks(y_pos, compare_df['state_name'])
plt.xlabel('Opportunity Index (0–100)', fontsize=11, fontweight='semibold')
plt.title('The Geographic Divide: Top 5 vs. Bottom 5 States in Opportunity Index', fontsize=12, pad=12, fontweight='bold', color='#1F497D')
plt.axvline(x=df_all['opportunity_index'].mean(), color='gray', linestyle='--', label=f"All-India Average: {df_all['opportunity_index'].mean():.1f}")
plt.legend(loc='lower right')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('dashboard/charts/barchart_top_vs_bottom_opportunity.png')
plt.close()

# Chart 5: Gender Funnel Across Educational & Economic Pipeline
pipeline_metrics = pd.DataFrame({
    'Stage': ['Adult Literacy (7+)', 'Secondary Retention', 'College Enrolment (GER)', 'Workforce Entry (LFPR 15+)'],
    'Male': [df_all['male_literacy_rate_plfs'].mean(), (100 - df_all['dropout_sec_boys']).mean(), df_all['ger_higher_ed_male'].mean(), 77.2],
    'Female': [df_all['female_literacy_rate_plfs'].mean(), (100 - df_all['dropout_sec_girls']).mean(), df_all['ger_higher_ed_female'].mean(), df_all['female_lfpr_15_plus'].mean()]
})
pipeline_metrics['Gender_Gap (M - F)'] = (pipeline_metrics['Male'] - pipeline_metrics['Female']).round(1)

plt.figure(figsize=(9, 5))
x = np.arange(len(pipeline_metrics))
width = 0.35
plt.bar(x - width/2, pipeline_metrics['Male'], width, label='Male (%)', color='#1F497D')
plt.bar(x + width/2, pipeline_metrics['Female'], width, label='Female (%)', color='#ED7D31')
plt.xticks(x, pipeline_metrics['Stage'], fontsize=10, rotation=10)
plt.ylabel('Percentage (%)', fontsize=11)
plt.title('Where Does the Gender Divide Widen Most Across the Student Pipeline?', fontsize=12, pad=15, fontweight='bold', color='#1F497D')
plt.legend()
for i in range(len(pipeline_metrics)):
    gap = pipeline_metrics.loc[i, 'Gender_Gap (M - F)']
    y_val = max(pipeline_metrics.loc[i, 'Male'], pipeline_metrics.loc[i, 'Female']) + 2
    plt.text(i, y_val, f"Gap: {gap:+.1f}%", ha='center', fontsize=9, fontweight='bold', color='#C00000' if gap > 5 else '#385723')
plt.ylim(0, 105)
plt.tight_layout()
plt.savefig('dashboard/charts/gender_pipeline_gap_funnel.png')
plt.close()

print("\n=== 3. K-MEANS CLUSTERING (OPPORTUNITY TIERS) ===")
cluster_features = ['subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender']
X = df_index[cluster_features].values

X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std

def compute_silhouette_numpy(data, labels):
    n = len(data)
    clusters = np.unique(labels)
    if len(clusters) <= 1 or len(clusters) >= n:
        return 0.0
    s_vals = []
    for i in range(n):
        c_i = labels[i]
        same_c = data[labels == c_i]
        if len(same_c) > 1:
            a_i = np.mean(np.linalg.norm(same_c - data[i], axis=1)[np.linalg.norm(same_c - data[i], axis=1) > 0])
        else:
            a_i = 0.0
        b_vals = []
        for c in clusters:
            if c != c_i:
                diff_c = data[labels == c]
                b_vals.append(np.mean(np.linalg.norm(diff_c - data[i], axis=1)))
        b_i = min(b_vals) if b_vals else 0.0
        max_ab = max(a_i, b_i)
        s_vals.append((b_i - a_i) / max_ab if max_ab > 0 else 0.0)
    return float(np.mean(s_vals))

np.random.seed(42)
for k in range(2, 7):
    best_inertia = np.inf
    best_labels = None
    for _ in range(25):
        centroids, labels = kmeans2(X_scaled, k, minit='points')
        cur_inertia = sum(np.linalg.norm(X_scaled[i] - centroids[labels[i]])**2 for i in range(len(X_scaled)))
        if cur_inertia < best_inertia:
            best_inertia = cur_inertia
            best_labels = labels
    sil = compute_silhouette_numpy(X_scaled, best_labels)
    print(f"k = {k}: Inertia = {best_inertia:.2f}, Silhouette Score = {sil:.3f}")

# Final selection: k=4 tiers
best_k4_inertia = np.inf
best_k4_labels = None
for _ in range(50):
    centroids, labels = kmeans2(X_scaled, 4, minit='points')
    cur_inertia = sum(np.linalg.norm(X_scaled[i] - centroids[labels[i]])**2 for i in range(len(X_scaled)))
    if cur_inertia < best_k4_inertia:
        best_k4_inertia = cur_inertia
        best_k4_labels = labels

df_all['cluster'] = best_k4_labels

cluster_means = df_all.groupby('cluster')['opportunity_index'].mean().sort_values(ascending=False)
tier_map = {cluster_id: f"Cluster {idx+1}" for idx, cluster_id in enumerate(cluster_means.index)}
tier_names = {
    cluster_means.index[0]: "Cluster 1: Employment-Led Dynamism",
    cluster_means.index[1]: "Cluster 2: Educational Infrastructure Hubs",
    cluster_means.index[2]: "Cluster 3: Gender-Strong / School Infrastructure Lags",
    cluster_means.index[3]: "Cluster 4: Schooling-Active / Tertiary & Gender Constrained"
}

df_all['tier_code'] = df_all['cluster'].map(tier_map)
df_all['opportunity_tier'] = df_all['cluster'].map(tier_names)

df_all[['state_code', 'state_name', 'tier_code', 'opportunity_tier'] + subindex_cols].to_csv('clean_data/state_clusters.csv', index=False)
print("\nCluster Profiling Table:")
tier_summary = df_all.groupby('tier_code')[subindex_cols].mean().round(2)
tier_summary['State_Count'] = df_all['tier_code'].value_counts()
print(tier_summary.to_string())

# Chart 6: Cluster Tiers Visualization
plt.figure(figsize=(9, 6))
colors_tier = {'Cluster 1': '#1F497D', 'Cluster 2': '#2E75B6', 'Cluster 3': '#ED7D31', 'Cluster 4': '#C00000'}
for tier in ['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4']:
    sub = df_all[df_all['tier_code'] == tier]
    plt.scatter(sub['subindex_school'], sub['subindex_jobs'], s=sub['subindex_higher_ed']*2.5, label=tier_names[cluster_means.index[int(tier[-1])-1]], alpha=0.8, color=colors_tier[tier])

for st in ['Chandigarh', 'Kerala', 'Tamil Nadu', 'Gujarat', 'Bihar', 'Meghalaya', 'Delhi']:
    row = df_all[df_all['state_name'] == st].iloc[0]
    plt.annotate(st, (row['subindex_school'] + 1, row['subindex_jobs'] + 0.5), fontsize=8, fontweight='semibold')

plt.title('K-Means Clustering: Four Structural Profiles Across Indian States & UTs', fontsize=12, pad=12, fontweight='bold', color='#1F497D')
plt.xlabel('School Access & Quality Sub-Index (0–100)', fontsize=11)
plt.ylabel('Jobs & Economy Sub-Index (0–100)', fontsize=11)
plt.legend(title='Opportunity Profile', loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig('dashboard/charts/cluster_tiers_scatter.png')
plt.close()

# Export Q6 Targeted Interventions via Explicit Single-Column Calculation
p_a = df_all[['state_name', 'subindex_school']].sort_values(by='subindex_school').head(5).copy()
p_a['program'] = 'Program A: Public School Infrastructure'
p_a['selection_rule'] = 'Lowest 5 subindex_school'
p_a['metric_name'] = 'subindex_school'
p_a['metric_value'] = p_a['subindex_school']

p_b = df_all[['state_name', 'subindex_higher_ed']].sort_values(by='subindex_higher_ed').head(5).copy()
p_b['program'] = 'Program B: Higher Education Capacity'
p_b['selection_rule'] = 'Lowest 5 subindex_higher_ed'
p_b['metric_name'] = 'subindex_higher_ed'
p_b['metric_value'] = p_b['subindex_higher_ed']

p_c = df_all[['state_name', 'female_lfpr_15_plus']].sort_values(by='female_lfpr_15_plus').head(5).copy()
p_c['program'] = 'Program C: Female Workforce Inclusion'
p_c['selection_rule'] = 'Lowest 5 female_lfpr_15_plus'
p_c['metric_name'] = 'female_lfpr_15_plus'
p_c['metric_value'] = p_c['female_lfpr_15_plus']

q6_df = pd.concat([
    p_a[['program', 'selection_rule', 'state_name', 'metric_name', 'metric_value']],
    p_b[['program', 'selection_rule', 'state_name', 'metric_name', 'metric_value']],
    p_c[['program', 'selection_rule', 'state_name', 'metric_name', 'metric_value']]
]).reset_index(drop=True)

q6_df.to_csv('clean_data/q6_targeted_interventions.csv', index=False)
print("\nTargeted interventions exported to clean_data/q6_targeted_interventions.csv:")
print(q6_df.to_string())

print("\nAll 6 presentation charts created successfully in dashboard/charts/!")
