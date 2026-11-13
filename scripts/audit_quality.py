import pandas as pd
import numpy as np

df = pd.read_csv('clean_data/state_master.csv')
print("=== DATA QUALITY REPORT ===")
print(f"Total Rows: {len(df)}")
print(f"Total Columns: {len(df.columns)}")
print(f"Total Missing Values: {df.isnull().sum().sum()}")

num_cols = df.select_dtypes(include=[np.number]).columns
outlier_dict = {}
for col in num_cols:
    s = df[col]
    q25 = s.quantile(0.25)
    q75 = s.quantile(0.75)
    iqr = q75 - q25
    low_bound = q25 - 1.5 * iqr
    high_bound = q75 + 1.5 * iqr
    outliers = df[(s < low_bound) | (s > high_bound)][['state_name', col]].to_dict(orient='records')
    outlier_dict[col] = {
        'min': s.min(),
        'max': s.max(),
        'mean': round(s.mean(), 2),
        'median': round(s.median(), 2),
        'std': round(s.std(), 2),
        'outliers': outliers
    }
    out_str = ', '.join([f"{o['state_name']} ({o[col]})" for o in outliers]) if outliers else 'None'
    print(f"{col}: Min={s.min()}, Max={s.max()}, Mean={round(s.mean(),2)}, Median={round(s.median(),2)} | Outliers: {out_str}")

