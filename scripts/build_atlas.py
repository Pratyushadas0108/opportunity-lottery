"""
Builds the Opportunity Atlas interactive web application in atlas/index.html.
Embeds all clean data and provides an interactive map, ranking leaderboard,
gender funnel, cluster profiling, and policy recommendations.
"""

import json
import pandas as pd

# Load data
df_idx = pd.read_csv('clean_data/opportunity_index.csv')
df_mast = pd.read_csv('clean_data/state_master.csv')
df_clust = pd.read_csv('clean_data/state_clusters.csv')
df_q6 = pd.read_csv('clean_data/q6_targeted_interventions.csv')

# Merge
df = df_idx.merge(df_clust[['state_name', 'tier_code', 'opportunity_tier']], on='state_name')
df.rename(columns={'tier_code': 'cluster_code', 'opportunity_tier': 'cluster_profile'}, inplace=True)

# Add 28-states rank
df_states = df[df['entity_type'] == 'State'].sort_values(by='opportunity_index', ascending=False).reset_index(drop=True)
df_states['rank_states_28'] = df_states.index + 1
df = df.merge(df_states[['state_name', 'rank_states_28']], on='state_name', how='left')

# Region mapping
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

# Key raw indicators
raw_cols = [
    'transition_rate_upprim_to_sec', 'dropout_sec_total', 'dropout_sec_boys', 'dropout_sec_girls',
    'pct_schools_electricity', 'ger_higher_ed_total', 'ger_higher_ed_male', 'ger_higher_ed_female',
    'gpi_higher_ed', 'colleges_per_lakh_pop', 'ptr_higher_ed', 'youth_unemployment_rate_15_29',
    'female_lfpr_15_plus', 'regular_wage_salaried_share', 'female_literacy_rate_plfs', 'male_literacy_rate_plfs',
    'urban_population_pct_2011'
]
df = df.merge(df_mast[['state_name'] + raw_cols], on='state_name')

# Convert to JSON records
states_data = df.to_dict(orient='records')
states_json = json.dumps(states_data, indent=2)
q6_json = json.dumps(df_q6.to_dict(orient='records'), indent=2)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Opportunity Atlas | Indian States Opportunity Index</title>
  <style>
    :root {{
      --primary: #1F497D;
      --primary-light: #2E75B6;
      --accent: #00B0F0;
      --bg: #F4F6F9;
      --card-bg: #FFFFFF;
      --text: #262626;
      --text-muted: #666666;
      --border: #E0E4E8;
      --red: #C00000;
      --green: #385723;
      --gold: #C65911;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); line-height: 1.5; }}
    
    header {{
      background: linear-gradient(135deg, #1F497D 0%, #112A46 100%);
      color: white; padding: 2rem 1.5rem; text-align: center;
      border-bottom: 4px solid var(--accent);
    }}
    header h1 {{ font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.5px; }}
    header p {{ font-size: 1.05rem; opacity: 0.9; max-width: 850px; margin: 0 auto; }}
    .badge {{ display: inline-block; background: rgba(255,255,255,0.15); padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; margin-top: 0.75rem; }}

    nav {{
      background: white; border-bottom: 1px solid var(--border);
      position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }}
    .nav-container {{ max-width: 1200px; margin: 0 auto; display: flex; gap: 1rem; padding: 0 1rem; overflow-x: auto; }}
    .nav-btn {{
      padding: 0.85rem 1.25rem; font-size: 0.95rem; font-weight: 600; color: var(--text-muted);
      border: none; background: none; cursor: pointer; border-bottom: 3px solid transparent;
      white-space: nowrap; transition: all 0.2s;
    }}
    .nav-btn.active {{ color: var(--primary); border-bottom-color: var(--primary); }}
    .nav-btn:hover {{ color: var(--primary); }}

    main {{ max-width: 1200px; margin: 1.5rem auto; padding: 0 1rem; }}
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    .kpi-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1rem; margin-bottom: 1.5rem;
    }}
    .kpi-card {{
      background: var(--card-bg); padding: 1.25rem; border-radius: 8px;
      border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .kpi-card .label {{ font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem; }}
    .kpi-card .value {{ font-size: 1.8rem; font-weight: 700; color: var(--primary); }}
    .kpi-card .sub {{ font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem; }}

    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
    @media (max-width: 900px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

    .card {{
      background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border);
      padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .card h2 {{ font-size: 1.3rem; font-weight: 700; color: var(--primary); margin-bottom: 1rem; }}
    
    .filter-bar {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; align-items: center; }}
    select, input {{
      padding: 0.5rem 0.75rem; border: 1px solid var(--border); border-radius: 6px;
      font-size: 0.9rem; background: white;
    }}

    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; margin-top: 0.5rem; }}
    th, td {{ padding: 0.65rem 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }}
    th {{ background: #F8FAFC; font-weight: 600; color: var(--primary); position: sticky; top: 0; }}
    tr:hover {{ background: #F1F5F9; cursor: pointer; }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    
    .score-pill {{
      display: inline-block; padding: 0.2rem 0.55rem; border-radius: 12px;
      font-weight: 600; font-size: 0.8rem; color: white;
    }}

    /* Detail Modal / Panel */
    .detail-panel {{
      background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px;
      padding: 1.25rem; margin-top: 1rem;
    }}
    .detail-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }}
    .detail-item {{ background: white; padding: 0.75rem; border-radius: 6px; border: 1px solid var(--border); }}
    .detail-item span {{ display: block; font-size: 0.75rem; color: var(--text-muted); }}
    .detail-item strong {{ font-size: 1.1rem; color: var(--primary); }}

    /* Funnel styles */
    .funnel-stage {{
      background: white; border: 1px solid var(--border); border-radius: 8px;
      padding: 1rem 1.25rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;
    }}
    .funnel-bar-container {{ flex-grow: 1; margin: 0 1.5rem; }}
    .funnel-bar {{ height: 18px; border-radius: 9px; display: flex; overflow: hidden; background: #E2E8F0; margin-top: 0.25rem; }}
    .funnel-bar .male {{ background: var(--primary); }}
    .funnel-bar .female {{ background: #D946EF; }}

    .insight-card {{
      background: white; border-left: 4px solid var(--primary); border-radius: 0 8px 8px 0;
      padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .insight-card h3 {{ font-size: 1.05rem; font-weight: 700; color: var(--primary); margin-bottom: 0.4rem; }}
    .insight-card p {{ font-size: 0.92rem; color: #374151; }}
    .insight-card .caveat {{ font-size: 0.82rem; color: var(--text-muted); font-style: italic; margin-top: 0.4rem; }}

    footer {{ text-align: center; padding: 2rem; font-size: 0.85rem; color: var(--text-muted); border-top: 1px solid var(--border); margin-top: 3rem; }}
  </style>
</head>
<body>

<header>
  <h1>THE OPPORTUNITY ATLAS</h1>
  <p>Assessing Student Opportunity Disparities Across Indian States & Union Territories</p>
  <div class="badge">Official Data: UDISE+ AY 2024–25 | AISHE AY 2023–24 | PLFS CY 2025 | Census 2011</div>
</header>

<nav>
  <div class="nav-container">
    <button class="nav-btn active" onclick="showTab('leaderboard')">State Rankings</button>
    <button class="nav-btn" onclick="showTab('pipeline')">Pipeline Breakdown</button>
    <button class="nav-btn" onclick="showTab('gender')">The Gender Funnel</button>
    <button class="nav-btn" onclick="showTab('clusters')">Structural Profiles</button>
    <button class="nav-btn" onclick="showTab('insights')">Insights & Policy</button>
  </div>
</nav>

<main>
  <!-- TOP KPIS -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="label">All-India Mean Score</div>
      <div class="value">54.49</div>
      <div class="sub">Across 36 States & UTs (Std Dev: 7.83)</div>
    </div>
    <div class="kpi-card">
      <div class="label">#1 Overall Entity</div>
      <div class="value">Chandigarh</div>
      <div class="sub">Score: 70.05 (Universal Schooling & Electrification)</div>
    </div>
    <div class="kpi-card">
      <div class="label">#1 Major State (>10M Pop)</div>
      <div class="value">Tamil Nadu</div>
      <div class="sub">Score: 64.92 (#2 among 28 full states)</div>
    </div>
    <div class="kpi-card">
      <div class="label">Top 5 vs Bottom 5 Divide</div>
      <div class="value">25.32 pts</div>
      <div class="sub">Top 5 (67.82) is 1.60x higher than Bottom 5 (42.50)</div>
    </div>
  </div>

  <!-- TAB 1: LEADERBOARD -->
  <div id="leaderboard" class="tab-content active">
    <div class="card">
      <h2>State Opportunity Leaderboard</h2>
      <div class="filter-bar">
        <label>View Framework: 
          <select id="frameworkFilter" onchange="filterData()">
            <option value="all">All 36 States & UTs</option>
            <option value="states">28 States Only</option>
          </select>
        </label>
        <label>Region:
          <select id="regionFilter" onchange="filterData()">
            <option value="all">All Regions</option>
            <option value="North">North</option>
            <option value="South">South</option>
            <option value="East">East</option>
            <option value="West">West</option>
            <option value="Central">Central</option>
            <option value="North-East">North-East</option>
          </select>
        </label>
        <input type="text" id="searchInput" placeholder="Search state..." onkeyup="filterData()">
      </div>

      <div style="max-height: 480px; overflow-y: auto;">
        <table id="rankTable">
          <thead>
            <tr>
              <th style="width: 60px;">Rank</th>
              <th>State / UT</th>
              <th>Entity</th>
              <th>Region</th>
              <th class="num">School (25%)</th>
              <th class="num">Higher Ed (25%)</th>
              <th class="num">Jobs (25%)</th>
              <th class="num">Gender (25%)</th>
              <th class="num">Opportunity Index</th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>

      <!-- State Inspector Panel -->
      <div id="inspectorPanel" class="detail-panel" style="display:none;">
        <h3 id="inspectStateName" style="color:var(--primary); font-size:1.2rem;"></h3>
        <p id="inspectClusterProfile" style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;"></p>
        <div class="detail-grid">
          <div class="detail-item"><span>School Transition Rate</span><strong id="inspectTrans"></strong></div>
          <div class="detail-item"><span>School Electrification</span><strong id="inspectElec"></strong></div>
          <div class="detail-item"><span>College GER (18–23)</span><strong id="inspectGER"></strong></div>
          <div class="detail-item"><span>College Density</span><strong id="inspectDensity"></strong></div>
          <div class="detail-item"><span>Youth Unemployment</span><strong id="inspectUR"></strong></div>
          <div class="detail-item"><span>Female LFPR (15+)</span><strong id="inspectLFPR"></strong></div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 2: PIPELINE BREAKDOWN -->
  <div id="pipeline" class="tab-content">
    <div class="card">
      <h2>Progression Pipeline Continuity Analysis</h2>
      <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.5rem;">
        Testing whether strength at one transition stage translates into strength at the next stage across 36 macro administrative entities.
      </p>
      
      <div class="two-col">
        <div style="background:#F8FAFC; padding:1.25rem; border-radius:8px; border:1px solid var(--border);">
          <h3 style="color:var(--primary); font-size:1.1rem; margin-bottom:0.5rem;">Link 1: School Quality $\leftrightarrow$ Higher Education</h3>
          <div style="font-size:1.8rem; font-weight:700; color:var(--green); margin-bottom:0.5rem;">r = +0.512 (Moderate-to-Strong)</div>
          <p style="font-size:0.88rem; color:#4B5563;">
            States with strong public school infrastructure, low dropout rates, and high secondary transition systematically co-occur with higher tertiary enrolment (e.g., Tamil Nadu, Kerala, Chandigarh).
          </p>
        </div>

        <div style="background:#F8FAFC; padding:1.25rem; border-radius:8px; border:1px solid var(--border);">
          <h3 style="color:var(--primary); font-size:1.1rem; margin-bottom:0.5rem;">Link 2: Higher Education $\leftrightarrow$ Youth Jobs</h3>
          <div style="font-size:1.8rem; font-weight:700; color:var(--gold); margin-bottom:0.5rem;">r = +0.058 (No Linear Link)</div>
          <p style="font-size:0.88rem; color:#4B5563;">
            Tertiary expansion shows no clear linear correlation with immediate youth employment dynamism in cross-sectional data. Educated youth often experience longer search queues for formal jobs rather than accepting informal work.
          </p>
        </div>
      </div>

      <div style="margin-top:2rem;">
        <h3 style="color:var(--primary); font-size:1.1rem; margin-bottom:1rem;">The Two Pipeline Extremes</h3>
        <div class="two-col">
          <div class="detail-item" style="border-left:4px solid var(--primary);">
            <strong style="color:var(--primary);">Kerala (Education Peak, Jobs Friction)</strong>
            <p style="font-size:0.85rem; margin-top:0.25rem;">School Rank: #2 (91.66) | College Rank: #6 (58.96)<br>Jobs Rank: #27 (49.09) | Youth Unemployment: 20.8%</p>
          </div>
          <div class="detail-item" style="border-left:4px solid var(--green);">
            <strong style="color:var(--green);">Gujarat (Industrial Dynamism, Lower College Enrolment)</strong>
            <p style="font-size:0.85rem; margin-top:0.25rem;">Jobs Rank: #1 Major State (79.95) | Youth Unemployment: 2.5%<br>College Rank: #21 (40.02) | College GER: 26.5%</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 3: THE GENDER FUNNEL -->
  <div id="gender" class="tab-content">
    <div class="card">
      <h2>The Gender Progression Funnel</h2>
      <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.5rem;">
        Tracking where gender disparities narrow, reverse, and reappear across four sequential stages of life.
      </p>

      <div class="funnel-stage">
        <div style="width: 220px;">
          <strong>Stage 1: Adult Literacy</strong>
          <span style="display:block; font-size:0.75rem; color:var(--text-muted);">Age 7+ (PLFS CY 2025)</span>
        </div>
        <div class="funnel-bar-container">
          <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
            <span>Male: 87.5% (Official) / 90.5% (Mean)</span>
            <span>Female: 74.9% (Official) / 80.5% (Mean)</span>
          </div>
          <div class="funnel-bar">
            <div class="male" style="width: 53%;"></div>
            <div class="female" style="width: 47%;"></div>
          </div>
        </div>
        <div style="width: 140px; text-align:right;">
          <strong style="color:var(--primary);">+10.0 to 12.6 pp</strong>
          <span style="display:block; font-size:0.75rem; color:var(--text-muted);">Male Lead</span>
        </div>
      </div>

      <div class="funnel-stage">
        <div style="width: 220px;">
          <strong>Stage 2: Secondary Retention</strong>
          <span style="display:block; font-size:0.75rem; color:var(--text-muted);">Class 9–10 (UDISE+ AY 2024–25)</span>
        </div>
        <div class="funnel-bar-container">
          <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
            <span>Boys: 86.7% (Official) / 87.3% (Mean)</span>
            <span>Girls: 90.4% (Official) / 90.8% (Mean)</span>
          </div>
          <div class="funnel-bar">
            <div class="male" style="width: 49%;"></div>
            <div class="female" style="width: 51%;"></div>
          </div>
        </div>
        <div style="width: 140px; text-align:right;">
          <strong style="color:#D946EF;">-3.5 to 3.7 pp</strong>
          <span style="display:block; font-size:0.75rem; color:#D946EF; font-weight:600;">Female Lead</span>
        </div>
      </div>

      <div class="funnel-stage">
        <div style="width: 220px;">
          <strong>Stage 3: College Enrolment</strong>
          <span style="display:block; font-size:0.75rem; color:var(--text-muted);">GER 18–23 (AISHE AY 2023–24)</span>
        </div>
        <div class="funnel-bar-container">
          <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
            <span>Male: 28.9% (Official) / 29.8% (Mean)</span>
            <span>Female: 31.2% (Official) / 34.3% (Mean)</span>
          </div>
          <div class="funnel-bar">
            <div class="male" style="width: 48%;"></div>
            <div class="female" style="width: 52%;"></div>
          </div>
        </div>
        <div style="width: 140px; text-align:right;">
          <strong style="color:#D946EF;">-2.3 to 4.5 pp</strong>
          <span style="display:block; font-size:0.75rem; color:#D946EF; font-weight:600;">Female Lead</span>
        </div>
      </div>

      <div class="funnel-stage" style="border-left:4px solid var(--red);">
        <div style="width: 220px;">
          <strong>Stage 4: Workforce Entry</strong>
          <span style="display:block; font-size:0.75rem; color:var(--text-muted);">LFPR 15+ years (PLFS CY 2025)</span>
        </div>
        <div class="funnel-bar-container">
          <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
            <span>Male: 79.1% (Official) / 77.2% (Mean)</span>
            <span>Female: 40.0% (Official) / 43.8% (Mean)</span>
          </div>
          <div class="funnel-bar">
            <div class="male" style="width: 65%;"></div>
            <div class="female" style="width: 35%;"></div>
          </div>
        </div>
        <div style="width: 140px; text-align:right;">
          <strong style="color:var(--red);">+33.4 to 39.1 pp</strong>
          <span style="display:block; font-size:0.75rem; color:var(--red); font-weight:600;">Substantial Gap</span>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 4: CLUSTERS -->
  <div id="clusters" class="tab-content">
    <div class="card">
      <h2>Unsupervised Clustering: Four Structural Profiles ($k=4$)</h2>
      <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.5rem;">
        K-means clustering across the four sub-indices groups states into descriptive structural profiles based on dimensional trade-offs.
      </p>

      <div class="kpi-grid">
        <div class="kpi-card" style="border-top:4px solid #1F497D;">
          <div class="label">Cluster 1 (4 States/UTs)</div>
          <div class="value" style="font-size:1.3rem;">Employment-Led Dynamism</div>
          <div class="sub">Mean Jobs: <strong>78.65</strong> | Higher Ed: 40.03 | School: 69.56</div>
          <p style="font-size:0.8rem; margin-top:0.5rem; color:var(--text-muted);">D&NH and D&D, Sikkim, Gujarat, Chhattisgarh</p>
        </div>

        <div class="kpi-card" style="border-top:4px solid #2E75B6;">
          <div class="label">Cluster 2 (15 States/UTs)</div>
          <div class="value" style="font-size:1.3rem;">Educational Hubs</div>
          <div class="sub">Mean School: <strong>83.31</strong> | Higher Ed: <strong>57.48</strong> | Jobs: 52.42</div>
          <p style="font-size:0.8rem; margin-top:0.5rem; color:var(--text-muted);">Chandigarh, Puducherry, Tamil Nadu, Kerala, Karnataka, Himachal, Delhi, Maharashtra, etc.</p>
        </div>

        <div class="kpi-card" style="border-top:4px solid #ED7D31;">
          <div class="label">Cluster 3 (9 States/UTs)</div>
          <div class="value" style="font-size:1.3rem;">Gender-Strong / School Lags</div>
          <div class="sub">Mean Gender: <strong>55.16</strong> | Lowest School: <strong>50.64</strong> | Higher Ed: 40.42</div>
          <p style="font-size:0.8rem; margin-top:0.5rem; color:var(--text-muted);">Meghalaya, Arunachal, Manipur, Mizoram, Nagaland, Assam, Tripura, Ladakh, West Bengal</p>
        </div>

        <div class="kpi-card" style="border-top:4px solid #C00000;">
          <div class="label">Cluster 4 (8 States/UTs)</div>
          <div class="value" style="font-size:1.3rem;">School-Led / Tertiary Constrained</div>
          <div class="sub">School: <strong>62.02</strong> | Lowest Higher Ed: <strong>36.33</strong> | Lowest Gender: <strong>39.36</strong></div>
          <p style="font-size:0.8rem; margin-top:0.5rem; color:var(--text-muted);">Bihar, Uttar Pradesh, Jharkhand, Rajasthan, Madhya Pradesh, Odisha, J&K, Andaman & Nicobar</p>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 5: INSIGHTS & POLICY -->
  <div id="insights" class="tab-content">
    <div class="card">
      <h2>The Analyst's Five Core Empirical Insights</h2>
      
      <div class="insight-card">
        <h3>1. A 25-point gap separates the top and bottom of the opportunity index</h3>
        <p>Across 36 states and UTs, the top five average 67.8 and the bottom five 42.5. Among the 28 full states, Sikkim ranks first, with Tamil Nadu as the highest-ranked large state, and Bihar is last at 35.5. The ranking holds under three alternative weighting scenarios (four weighting schemes in total, Spearman $\rho \ge 0.90$).</p>
        <div class="caveat">Caveat: This is a relative index built from data of different years, so it ranks states against each other and says nothing about absolute levels.</div>
      </div>

      <div class="insight-card">
        <h3>2. The gender gap appears at work, not in school</h3>
        <p>Girls drop out of secondary school less than boys (9.6% vs 13.3%, UDISE+ AY 2024–25) and have a higher college enrolment ratio (31.2 vs 28.9, AISHE AY 2023–24). Yet male labour force participation is 79.1% against 40.0% for women, a 39.1 percentage point gap (PLFS CY 2025).</p>
        <div class="caveat">Caveat: Three different years and sources, and participation covers all women aged 15+, not only graduates.</div>
      </div>

      <div class="insight-card">
        <h3>3. Better school and college access go together, but neither lines up with youth job outcomes</h3>
        <p>School and higher-education scores are moderately correlated (r = 0.51), while higher-education access and youth job scores show almost no relationship (r = 0.06). Kerala ranks near the top for schools and colleges but 27th on jobs, with youth unemployment of about 20.8%. Gujarat is first on jobs with 2.5% youth unemployment, yet 21st in college enrolment.</p>
        <div class="caveat">Caveat: Only 36 observations, and half the jobs index is based on unemployment. Educated youth searching for better jobs and out-migration are possible explanations that this data cannot test.</div>
      </div>

      <div class="insight-card">
        <h3>4. Two states can have the same score and need different help</h3>
        <p>Clusters 3 and 4 have nearly identical composite scores (48.0 and 47.1), but different shapes. The first (mostly northeastern and hill states) is relatively strong on gender (55.2) and weak on schools (50.6). The second (including Bihar, UP, and Rajasthan) has better schools (62.0) but the weakest higher education (36.3) and gender scores (39.4). Meghalaya shows the same pattern: a top-tier gender score (64.8) alongside school electrification of only 28.1%.</p>
        <div class="caveat">Caveat: Clusters are statistical groupings from k-means with k=4 and are not official categories.</div>
      </div>

      <div class="insight-card">
        <h3>5. Higher literacy and urbanization do not guarantee higher female labour participation</h3>
        <p>Delhi is 97.5% urban with female literacy of 84.4%, yet it has the lowest female labour force participation in the country at 13.1%. Among full states, Haryana (23.8%) and Bihar (24.7%) are lowest.</p>
        <div class="caveat">Caveat: This describes a pattern in survey data, and the reasons (job availability, safety, social norms, how work is measured) are outside what this project tested.</div>
      </div>
    </div>

    <div class="card">
      <h2>Targeted Policy Recommendations</h2>
      
      <div class="insight-card" style="border-left-color:var(--green);">
        <h3>Recommendation 1: Public School Infrastructure Funding</h3>
        <p><strong>Target States (5 lowest School Access scores):</strong> Meghalaya (15.74), Arunachal Pradesh (38.70), Bihar (48.27), Manipur (50.18), Mizoram (50.84).</p>
        <p>Meghalaya’s electrification figure (28.1%) shows basic facilities are the binding constraint. Check district-level data before allocating money, since state averages hide significant local variation.</p>
      </div>

      <div class="insight-card" style="border-left-color:var(--primary-light);">
        <h3>Recommendation 2: College Capacity and Faculty Funding</h3>
        <p><strong>Target States (5 lowest Higher Ed Access scores):</strong> Bihar (28.26), Jharkhand (29.21), D&NH and D&D (31.58), Ladakh (32.89), Andaman & Nicobar (33.78).</p>
        <p>Focus college capacity and faculty funding on Bihar and Jharkhand first (Bihar has 61.3 students per teacher and only 8.07 colleges per lakh population). Small UTs on the same list probably need different solutions, such as scholarships to study elsewhere or distance learning options, because they cannot support many standalone colleges.</p>
      </div>

      <div class="insight-card" style="border-left-color:var(--gold);">
        <h3>Recommendation 3: Female Workforce Transition Support</h3>
        <p><strong>Target States (5 lowest Female LFPR):</strong> Delhi (13.1%), Lakshadweep (21.9%), Haryana (23.8%), Bihar (24.7%), Goa (27.4%).</p>
        <p>Pair skilling programs for women with job-access support (safe transit, childcare). Female literacy is already high in several of them, so the data suggests the barrier lies after education. Start with a pilot, track employment outcomes, and test local reasons before scaling.</p>
      </div>
    </div>
  </div>
</main>

<footer>
  <p><strong>The Opportunity Lottery</strong> | Portfolio Project by Pratyush Das (B.Tech CS, AI/ML Specialization)</p>
  <p>Code & Pipeline: <a href="https://github.com/Pratyushadas0108/opportunity-lottery" target="_blank" style="color:var(--primary);">GitHub Repository</a> | Data verified against official MoE & MoSPI publications.</p>
</footer>

<script>
  const statesData = {states_json};

  function getScoreColor(val) {{
    if (val >= 64) return '#1F497D'; // Top
    if (val >= 55) return '#2E75B6'; // High
    if (val >= 47) return '#ED7D31'; // Mid
    return '#C00000'; // Low
  }}

  function renderTable(data) {{
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    data.forEach((s) => {{
      const tr = document.createElement('tr');
      tr.onclick = () => inspectState(s);
      
      const rank = document.getElementById('frameworkFilter').value === 'states' ? s.rank_states_28 : s.rank_baseline;
      if (!rank) return;

      tr.innerHTML = `
        <td style="font-weight:700; color:var(--primary);">#${{rank}}</td>
        <td><strong>${{s.state_name}}</strong></td>
        <td><span style="font-size:0.75rem; color:var(--text-muted);">${{s.entity_type}}</span></td>
        <td><span style="font-size:0.75rem; color:var(--text-muted);">${{s.region}}</span></td>
        <td class="num">${{s.subindex_school.toFixed(1)}}</td>
        <td class="num">${{s.subindex_higher_ed.toFixed(1)}}</td>
        <td class="num">${{s.subindex_jobs.toFixed(1)}}</td>
        <td class="num">${{s.subindex_gender.toFixed(1)}}</td>
        <td class="num">
          <span class="score-pill" style="background:${{getScoreColor(s.opportunity_index)}}">
            ${{s.opportunity_index.toFixed(2)}}
          </span>
        </td>
      `;
      tbody.appendChild(tr);
    }});
  }}

  function filterData() {{
    const framework = document.getElementById('frameworkFilter').value;
    const region = document.getElementById('regionFilter').value;
    const search = document.getElementById('searchInput').value.toLowerCase();

    let filtered = statesData.filter(s => {{
      if (framework === 'states' && s.entity_type !== 'State') return false;
      if (region !== 'all' && s.region !== region) return false;
      if (search && !s.state_name.toLowerCase().includes(search)) return false;
      return true;
    }});

    if (framework === 'states') {{
      filtered.sort((a,b) => a.rank_states_28 - b.rank_states_28);
    }} else {{
      filtered.sort((a,b) => a.rank_baseline - b.rank_baseline);
    }}

    renderTable(filtered);
  }}

  function inspectState(s) {{
    const panel = document.getElementById('inspectorPanel');
    panel.style.display = 'block';
    document.getElementById('inspectStateName').innerText = `${{s.state_name}} (Overall Rank: #${{s.rank_baseline}} | Score: ${{s.opportunity_index.toFixed(2)}})`;
    document.getElementById('inspectClusterProfile').innerText = `Structural Profile: ${{s.cluster_profile}}`;
    document.getElementById('inspectTrans').innerText = `${{s.transition_rate_upprim_to_sec.toFixed(1)}}%`;
    document.getElementById('inspectElec').innerText = `${{s.pct_schools_electricity.toFixed(1)}}%`;
    document.getElementById('inspectGER').innerText = `${{s.ger_higher_ed_total.toFixed(1)}}%`;
    document.getElementById('inspectDensity').innerText = `${{s.colleges_per_lakh_pop.toFixed(1)}} / lakh`;
    document.getElementById('inspectUR').innerText = `${{s.youth_unemployment_rate_15_29.toFixed(1)}}%`;
    document.getElementById('inspectLFPR').innerText = `${{s.female_lfpr_15_plus.toFixed(1)}}%`;
    panel.scrollIntoView({{ behavior: 'smooth' }});
  }}

  function showTab(tabId) {{
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
  }}

  // Initial load
  filterData();
</script>

</body>
</html>
"""

with open('atlas/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Opportunity Atlas generated successfully at atlas/index.html!")
