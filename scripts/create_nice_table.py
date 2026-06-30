import sqlite3

conn = sqlite3.connect("db/drug_access.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS nice_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vmp_snomed_code TEXT,
    ta_number TEXT,
    drug_name TEXT,
    indication TEXT,
    decision_type TEXT,    -- recommended, not_recommended, optimised
    access_route TEXT,     -- standard_ta, cdf, hst, maa
    approval_date TEXT,    -- MHRA/EMA 승인일
    nice_decision_date TEXT,
    guidance_date TEXT,    -- 실제 NHS 적용일
    FOREIGN KEY (vmp_snomed_code) REFERENCES drugs(vmp_snomed_code)
)
""")

# 아달리무맙 NICE 데이터 수동 입력 (실제 TA 기준)
adalimumab_tas = [
    ("32888111000001102", "TA715", "Adalimumab", "Rheumatoid arthritis", "recommended", "standard_ta", "2000-09-01", "2021-08-18", "2021-08-18"),
    ("32888111000001102", "TA195", "Adalimumab", "Psoriatic arthritis", "recommended", "standard_ta", "2000-09-01", "2010-08-01", "2010-08-01"),
]

cur.executemany("""
INSERT OR IGNORE INTO nice_decisions
(vmp_snomed_code, ta_number, drug_name, indication, decision_type, access_route, approval_date, nice_decision_date, guidance_date)
VALUES (?,?,?,?,?,?,?,?,?)
""", adalimumab_tas)

conn.commit()
print(f"Inserted {cur.rowcount} NICE decisions.")

# 확인
cur.execute("SELECT ta_number, indication, nice_decision_date FROM nice_decisions")
for r in cur.fetchall():
    print(r)

conn.close()