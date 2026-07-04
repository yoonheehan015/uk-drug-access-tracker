import sqlite3
import pandas as pd
import os

# db 폴더 없으면 자동 생성
os.makedirs("db", exist_ok=True)

# DB 연결 (없으면 자동 생성)
conn = sqlite3.connect("db/drug_access.db")
cur = conn.cursor()

# 1. drugs 테이블
cur.execute("""
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vmp_snomed_code TEXT UNIQUE NOT NULL,
    vmp_product_name TEXT NOT NULL,
    access_route TEXT,
    therapy_area TEXT
)
""")

# 2. prescribing 테이블
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
conn.close()