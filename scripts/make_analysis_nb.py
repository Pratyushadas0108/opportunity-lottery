import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1: Overview
c1 = nbf.v4.new_markdown_cell("""# Notebook 03: Opportunity Analysis, Correlations & Tier Clustering
## The Opportunity Lottery: Statistical Disparities Across Indian States

**Objectives**:
1. **Correlation Analysis**: Quantify relationships between foundational schooling, tertiary expansion, labor market absorption, and gender parity.
2. **Pipeline Gap Analysis**: Measure disparities between Top 5 and Bottom 5 states, and trace where the gender divide widens most across the youth pipeline.
3. **Unsupervised Clustering (K-Means)**: Group 36 States & UTs into 4 distinct Opportunity Tiers based on empirical sub-index profiles, justified via Elbow & Silhouette metrics.
4. **Empirical Findings**: Synthesize hard numbers answering Business Questions 1 through 7 for student insight authoring.
""")

# Cell 2: Imports
c2 = nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.vq import kmeans2
from scipy import stats

# Load data
df_master = pd.read_csv('../clean_data/state_master.csv')
df_index = pd.read_csv('../clean_data/opportunity_index.csv')
df_all = df_index.merge(df_master.drop(columns=['state_code', 'entity_type']), on='state_name')

print(f'Analysis dataset loaded: {df_all.shape[0]} states/UTs.')
df_all.head(3)
""")

# Cell 3: Correlation Matrix
c3 = nbf.v4.new_code_cell("""subindex_cols = ['subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 'opportunity_index']
subindex_labels = ['School Quality', 'Higher Ed Access', 'Jobs & Economy', 'Gender Equality', 'Opportunity Index']

corr_pearson = df_index[subindex_cols].corr(method='pearson')
print('=== PEARSON CORRELATION MATRIX ===')
corr_pearson.round(3)
""")

# Cell 4: Top 5 vs Bottom 5 Gap Analysis
c4 = nbf.v4.new_code_cell("""top5 = df_all.head(5)
bottom5 = df_all.tail(5)

gap_df = pd.DataFrame({
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
gap_df['Absolute_Gap'] = (gap_df['Top_5_Mean'] - gap_df['Bottom_5_Mean']).round(2)
gap_df['Ratio_Top_to_Bottom'] = (gap_df['Top_5_Mean'] / gap_df['Bottom_5_Mean']).round(2)

print('=== TOP 5 VS BOTTOM 5 GAP TABLE ===')
gap_df.round(2)
""")

# Cell 5: Gender Pipeline Gap Analysis
c5 = nbf.v4.new_code_cell("""pipeline_metrics = pd.DataFrame({
    'Stage': ['Adult Literacy (7+)', 'Secondary Retention (100 - Dropout)', 'College Enrolment (GER)', 'Workforce Entry (LFPR 15+)'],
    'Male': [df_all['male_literacy_rate_plfs'].mean(), (100 - df_all['dropout_sec_boys']).mean(), df_all['ger_higher_ed_male'].mean(), 77.2],
    'Female': [df_all['female_literacy_rate_plfs'].mean(), (100 - df_all['dropout_sec_girls']).mean(), df_all['ger_higher_ed_female'].mean(), df_all['female_lfpr_15_plus'].mean()]
})
pipeline_metrics['Gender_Gap (M - F)'] = (pipeline_metrics['Male'] - pipeline_metrics['Female']).round(1)
print('=== GENDER FUNNEL METRICS ===')
pipeline_metrics
""")

# Cell 6: K-Means Clustering & Justification
c6 = nbf.v4.new_code_cell("""cluster_features = ['subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender']
X = df_index[cluster_features].values
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)

def compute_silhouette_numpy(data, labels):
    n = len(data)
    clusters = np.unique(labels)
    if len(clusters) <= 1 or len(clusters) >= n:
        return 0.0
    s_vals = []
    for i in range(n):
        c_i = labels[i]
        same_c = data[labels == c_i]
        a_i = np.mean(np.linalg.norm(same_c - data[i], axis=1)[np.linalg.norm(same_c - data[i], axis=1) > 0]) if len(same_c) > 1 else 0.0
        b_vals = [np.mean(np.linalg.norm(data[labels == c] - data[i], axis=1)) for c in clusters if c != c_i]
        b_i = min(b_vals) if b_vals else 0.0
        max_ab = max(a_i, b_i)
        s_vals.append((b_i - a_i) / max_ab if max_ab > 0 else 0.0)
    return float(np.mean(s_vals))

np.random.seed(42)
print('Evaluating K=2 to 6:')
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
    print(f'k = {k}: Inertia = {best_inertia:.2f}, Silhouette Score = {sil:.3f}')
""")

# Cell 7: Opportunity Tiers Profiling
c7 = nbf.v4.new_code_cell("""df_clusters = pd.read_csv('../clean_data/state_clusters.csv')
print('=== OPPORTUNITY TIERS SUMMARY ===')
df_clusters.groupby('tier_code')[['subindex_school', 'subindex_higher_ed', 'subindex_jobs', 'subindex_gender', 'opportunity_index']].mean().round(2)
""")

nb.cells = [c1, c2, c3, c4, c5, c6, c7]

with open('notebooks/03_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print('notebooks/03_analysis.ipynb created successfully!')

