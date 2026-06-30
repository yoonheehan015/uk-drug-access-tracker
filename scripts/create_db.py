import sqlite3
import pandas as pd

# DB 연결 (없으면 자동 생성)
conn = sqlite3.connect("db/drug_access.db")
cur = conn.cursor()

# 1. drugs 테이블 (약물 마스터)
cur.execute("""
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vmp_snomed_code TEXT UNIQUE NOT NULL,
    vmp_product_name TEXT NOT NULL,
    access_route TEXT,   -- biosimilar, orphan, cell_gene, cdf 등
    therapy_area TEXT    -- rheumatology, oncology 등
)
""")

# 2. prescribing 테이블 (SCMD 처방 데이터)
cur.execute("""
CREATE TABLE IF NOT EXISTS prescribing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year_month INTEGER NOT NULL,
    ods_code TEXT NOT NULL,
    vmp_snomed_code TEXT NOT NULL,
    unit_of_measure TEXT,
    total_quantity REAL,
    indicative_cost REAL,
    FOREIGN KEY (vmp_snomed_code) REFERENCES drugs(vmp_snomed_code)
)
""")

conn.commit()
print("DB and tables created.")

# 3. SCMD CSV 적재
df = pd.read_csv("data/raw/scmd_final_202503.csv")

# drugs 테이블에 unique 약물 먼저 넣기
drugs_df = df[['VMP_SNOMED_CODE', 'VMP_PRODUCT_NAME']].drop_duplicates()
drugs_df.columns = ['vmp_snomed_code', 'vmp_product_name']
drugs_df['access_route'] = None
drugs_df['therapy_area'] = None
drugs_df.to_sql('drugs', conn, if_exists='append', index=False)
print(f"Inserted {len(drugs_df)} drugs.")

# prescribing 테이블에 처방 데이터 넣기
prescribing_df = df[['YEAR_MONTH','ODS_CODE','VMP_SNOMED_CODE',
                      'UNIT_OF_MEASURE_NAME','TOTAL_QUANITY_IN_VMP_UNIT','INDICATIVE_COST']]
prescribing_df.columns = ['year_month','ods_code','vmp_snomed_code',
                           'unit_of_measure','total_quantity','indicative_cost']
prescribing_df.to_sql('prescribing', conn, if_exists='append', index=False)
print(f"Inserted {len(prescribing_df)} prescribing rows.")

conn.close()
print("Done.")