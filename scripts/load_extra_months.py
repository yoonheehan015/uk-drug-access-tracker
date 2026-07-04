import sqlite3
import pandas as pd
import glob
import os

# db 폴더 없으면 자동 생성
os.makedirs("db", exist_ok=True)

conn = sqlite3.connect("db/drug_access.db")

files = sorted(
    glob.glob("data/raw/scmd_final_2024*.csv") +
    glob.glob("data/raw/scmd_final_202501.csv") +
    glob.glob("data/raw/scmd_final_202502.csv")
)

for f in files:
    month = f.split("_")[-1].replace(".csv", "")
    print(f"Loading {month}...")
    df = pd.read_csv(f)

    p_df = df[['YEAR_MONTH', 'ODS_CODE', 'VMP_SNOMED_CODE',
               'UNIT_OF_MEASURE_NAME', 'TOTAL_QUANITY_IN_VMP_UNIT', 'INDICATIVE_COST']]
    p_df.columns = ['year_month', 'ods_code', 'vmp_snomed_code',
                    'unit_of_measure', 'total_quantity', 'indicative_cost']
    p_df.to_sql('prescribing', conn, if_exists='append', index=False)
    print(f"  → {len(p_df)} rows")

conn.close()
print("Done.")