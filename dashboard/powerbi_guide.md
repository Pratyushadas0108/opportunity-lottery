# Power BI Desktop Implementation Guide: The Opportunity Lottery

This step-by-step implementation guide provides everything needed to build a polished, 4-page interactive executive dashboard in **Power BI Desktop** using the clean dataset `dashboard/opportunity_powerbi_data.csv`.

---

## 1. Data Connection & Power Query Setup

1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Text/CSV** $\rightarrow$ Select `dashboard/opportunity_powerbi_data.csv`.
3. In the preview window, click **Transform Data** to open Power Query Editor.
4. Verify column data types:
   - `state_code`, `state_name`, `entity_type`, `cluster_code`, `cluster_profile`, `region`: **Text**
   - `rank_all_36`, `rank_states_28`: **Whole Number**
   - `opportunity_index`, `subindex_school`, `subindex_higher_ed`, `subindex_jobs`, `subindex_gender`: **Decimal Number**
   - All percentage columns (`transition_rate_upprim_to_sec`, `dropout_sec_total`, `ger_higher_ed_total`, `female_lfpr_15_plus`, etc.): **Decimal Number**
5. Click **Close & Apply**.
6. In the **Data View** (left pane):
   - Select column `state_name` $\rightarrow$ Under **Column Tools**, set **Data Category** to `State or Province`.

---

## 2. Key DAX Measures

Create a dedicated Measures Table:
1. Under the **Home** tab, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Create the following DAX measures:

### Core Index Measures
```dax
Avg Opportunity Index = 
ROUND(AVERAGE(opportunity_powerbi_data[opportunity_index]), 2)
```

```dax
Avg School Score = 
ROUND(AVERAGE(opportunity_powerbi_data[subindex_school]), 2)
```

```dax
Avg Higher Ed Score = 
ROUND(AVERAGE(opportunity_powerbi_data[subindex_higher_ed]), 2)
```

```dax
Avg Jobs Score = 
ROUND(AVERAGE(opportunity_powerbi_data[subindex_jobs]), 2)
```

```dax
Avg Gender Score = 
ROUND(AVERAGE(opportunity_powerbi_data[subindex_gender]), 2)
```

### Dynamic KPIs & Flags
```dax
Top State Name = 
CALCULATE(
    SELECTEDVALUE(opportunity_powerbi_data[state_name]),
    FILTER(opportunity_powerbi_data, opportunity_powerbi_data[rank_all_36] = 1)
)
```

```dax
Top Major State Name = 
CALCULATE(
    SELECTEDVALUE(opportunity_powerbi_data[state_name]),
    FILTER(opportunity_powerbi_data, opportunity_powerbi_data[rank_states_28] = 2) // Tamil Nadu
)
```

```dax
Divide Gap Points = 
VAR Top5Avg = CALCULATE(AVERAGE(opportunity_powerbi_data[opportunity_index]), opportunity_powerbi_data[rank_all_36] <= 5)
VAR Bottom5Avg = CALCULATE(AVERAGE(opportunity_powerbi_data[opportunity_index]), opportunity_powerbi_data[rank_all_36] >= 32)
RETURN ROUND(Top5Avg - Bottom5Avg, 2)
```

```dax
Divide Ratio = 
VAR Top5Avg = CALCULATE(AVERAGE(opportunity_powerbi_data[opportunity_index]), opportunity_powerbi_data[rank_all_36] <= 5)
VAR Bottom5Avg = CALCULATE(AVERAGE(opportunity_powerbi_data[opportunity_index]), opportunity_powerbi_data[rank_all_36] >= 32)
RETURN ROUND(DIVIDE(Top5Avg, Bottom5Avg), 2)
```

```dax
Performance Tier Flag = 
SWITCH(
    TRUE(),
    opportunity_powerbi_data[rank_all_36] <= 5, "Top 5 Benchmark",
    opportunity_powerbi_data[rank_all_36] >= 32, "Bottom 5 Bottleneck",
    "Middle 26 States"
)
```

```dax
Conditional Color Index = 
SWITCH(
    TRUE(),
    SELECTEDVALUE(opportunity_powerbi_data[rank_all_36]) <= 5, "#1F497D",   // Deep Navy Blue
    SELECTEDVALUE(opportunity_powerbi_data[rank_all_36]) >= 32, "#C00000",  // Deep Coral Red
    "#5B9BD5"                                                               // Slate Blue
)
```

```dax
Gender LFPR Gap (pp) = 
ROUND(AVERAGE(opportunity_powerbi_data[youth_lfpr_15_29]) - AVERAGE(opportunity_powerbi_data[female_lfpr_15_plus]), 1)
```

---

## 3. Page-by-Page Visual Layout Specifications

### Page 1: Executive Overview & Geographic Divide
- **Canvas Background**: Light Grey (`#F8F9FA`).
- **Header**: "THE OPPORTUNITY LOTTERY: State Opportunity Divide Across India" (Subtitle: "Analyzing 36 States and UTs Across Education, Employment, and Gender").
- **Top KPI Cards (Row 1)**:
  1. Card 1: `[Avg Opportunity Index]` (Title: "National Average Score", Subtitle: "54.49 / 100")
  2. Card 2: `[Top State Name]` (Title: "#1 Ranked Entity", Value: "Chandigarh (70.05)")
  3. Card 3: `[Top Major State Name]` (Title: "#1 Major State", Value: "Tamil Nadu (64.92)")
  4. Card 4: `[Divide Gap Points]` (Title: "Top 5 vs Bottom 5 Gap", Subtitle: "25.32 Index Points (1.60x)")
- **Left Slicers Pane**:
  - Slicer 1: `entity_type` (Tile: "All", "State", "Union Territory")
  - Slicer 2: `region` (Dropdown: North, South, East, West, Central, North-East)
  - Slicer 3: `cluster_profile` (Dropdown of 4 structural profiles)
- **Central Visual**: **Filled Map / Shape Map of India**:
  - Location: `state_name`
  - Color saturation: `opportunity_index` (Diverging gradient: `#C00000` Red $\rightarrow$ `#FFD966` Amber $\rightarrow$ `#1F497D` Blue)
  - Tooltips: `state_name`, `opportunity_index`, `subindex_school`, `subindex_higher_ed`, `subindex_jobs`, `subindex_gender`, `rank_all_36`.
- **Right Visual**: **Horizontal Clustered Bar Chart**:
  - Y-axis: `state_name` (sorted descending by `opportunity_index`)
  - X-axis: `opportunity_index`
  - Data Colors: Apply conditional formatting using Field Value $\rightarrow$ `[Conditional Color Index]`.

---

### Page 2: Sub-Index Divergence & The Pipeline Disconnect
- **Header**: "Progression Pipeline Continuity: School vs. Higher Ed vs. Youth Employment"
- **Top Visual (Left)**: **Scatter Plot (School Quality vs. College Access)**:
  - X-axis: `subindex_school` (0–100)
  - Y-axis: `subindex_higher_ed` (0–100)
  - Details: `state_name`
  - Legend: `region`
  - Size: `colleges_per_lakh_pop`
  - Trend Line: Add linear regression trend line ($r = +0.51$).
  - Callout Annotation: "Moderate-to-Strong positive correlation ($r = 0.51$). Strong schooling systematically co-occurs with higher college enrolment."
- **Top Visual (Right)**: **Scatter Plot (College Access vs. Youth Jobs)**:
  - X-axis: `subindex_higher_ed` (0–100)
  - Y-axis: `subindex_jobs` (0–100)
  - Details: `state_name`
  - Legend: `cluster_code`
  - Trend Line: Add linear regression trend line ($r = +0.06$).
  - Visual Outlier Callouts:
    * Kerala: Highlighted at top-left of jobs (High College 59.0, low Jobs 49.1, Youth UR: 20.8%).
    * Gujarat: Highlighted at bottom-right of higher ed (Jobs 79.95, College 40.02, Youth UR: 2.5%).
  - Callout Annotation: "No clear linear association ($r = 0.06$). Expanding college access does not automatically correlate with immediate youth employment dynamism."
- **Bottom Visual**: **Sub-Index Decomposition Matrix / Table**:
  - Rows: `state_name`
  - Values: `subindex_school`, `subindex_higher_ed`, `subindex_jobs`, `subindex_gender`, `opportunity_index`
  - Conditional Formatting: Background data bars for each sub-index.

---

### Page 3: The Gender Progression Funnel
- **Header**: "The Gender Funnel: Where Parity Narrows and Disappears"
- **Top Visual**: **The 4-Stage Progression Clustered Column Chart**:
  - X-axis: 4 Pipeline Stages:
    1. Adult Literacy (Age 7+)
    2. Secondary Retention (Class 9–10)
    3. Higher-Ed Enrolment (GER 18–23)
    4. Workforce Participation (LFPR 15+)
  - Series: Male vs Female rates (Official National benchmarks: Literacy 87.5% M vs 74.9% F; Retention 86.7% M vs 90.4% F; College GER 28.9% M vs 31.2% F; LFPR 79.1% M vs 40.0% F).
  - Callout Box: "Parity holds through schooling and college (where young women outperform young men by 3.5 to 4.5 percentage points), but collapses into a 39.1 percentage point gap upon workforce entry."
- **Bottom Left Visual**: **Scatter Plot (Urbanization vs. Female Workforce Participation)**:
  - X-axis: `urban_population_pct_2011`
  - Y-axis: `female_lfpr_15_plus`
  - Details: `state_name`
  - Outlier Spotlight: Delhi at 97.5% urban and 13.1% female LFPR.
- **Bottom Right Visual**: **State Gender Gap Comparison Bar Chart**:
  - Y-axis: `state_name`
  - X-axis: Difference (`youth_lfpr_15_29` minus `female_lfpr_15_plus`).

---

### Page 4: Policy Clusters & Targeted Capital Allocation
- **Header**: "Strategic Profiles & Targeted Capital Allocation"
- **Top Visual**: **K-Means Cluster Matrix (Bubble Chart)**:
  - X-axis: `subindex_school`
  - Y-axis: `subindex_jobs`
  - Size: `subindex_higher_ed`
  - Legend: `cluster_profile` (4 structural profiles clearly differentiated).
- **Bottom Visuals (3 Targeted Intervention Cards)**:
  - **Program A (School Infrastructure Fund)**: Table showing Top 5 candidate states sorted by lowest `subindex_school` (Meghalaya, Arunachal Pradesh, Bihar, Manipur, Mizoram).
  - **Program B (Higher Education Capacity Fund)**: Table showing Top 5 candidate states sorted by lowest `subindex_higher_ed` (Bihar, Jharkhand, D&NH and D&D, Ladakh, Andaman & Nicobar).
  - **Program C (Female Workforce Transition Fund)**: Table showing Top 5 candidate states sorted by lowest `female_lfpr_15_plus` (Delhi, Lakshadweep, Haryana, Bihar, Goa).
- **Side Card**: "The Analyst's Five Core Insights & Three Recommendations" (Text card highlighting your 5 insights and caveats).

---

## 4. Theme & Design Styling Palette
To deliver an executive, publication-grade appearance:
- **Primary Navy**: `#1F497D` (Headers, baseline metrics, Top 5)
- **Accent Blue**: `#2E75B6` (School & Higher Ed indicators)
- **Warning Amber**: `#ED7D31` (Moderate bottlenecks)
- **Alert Coral**: `#C00000` (Bottom 5, severe deficits)
- **Neutral Dark**: `#262626` (Body text)
- **Neutral Light**: `#F2F4F7` (Card backgrounds)
- **Font**: Segoe UI or Arial throughout.
