import os
os.makedirs("data/processed", exist_ok=True)
import sqlite3
import pandas as pd

conn = sqlite3.connect("db/drug_access.db")

# 1. 월별 트렌드
trend_df = pd.read_sql_query("""
SELECT 
    year_month,
    COUNT(DISTINCT ods_code) as trust_count,
    ROUND(SUM(total_quantity),1) as total_qty,
    ROUND(SUM(indicative_cost),0) as total_cost
FROM prescribing p
JOIN drugs d ON p.vmp_snomed_code = d.vmp_snomed_code
WHERE LOWER(d.vmp_product_name) LIKE '%adalimumab%'
GROUP BY year_month
ORDER BY year_month
""", conn)
trend_df.to_csv("data/processed/adalimumab_monthly_trend.csv", index=False)

# 2. Trust별 상세 (지역 분석용)
trust_df = pd.read_sql_query("""
SELECT 
    p.year_month,
    p.ods_code,
    d.vmp_product_name,
    SUM(p.total_quantity) as total_qty,
    SUM(p.indicative_cost) as total_cost
FROM prescribing p
JOIN drugs d ON p.vmp_snomed_code = d.vmp_snomed_code
WHERE LOWER(d.vmp_product_name) LIKE '%adalimumab%'
GROUP BY p.year_month, p.ods_code, d.vmp_product_name
""", conn)
trust_df.to_csv("data/processed/adalimumab_by_trust.csv", index=False)

# 3. NICE 결정 데이터
nice_df = pd.read_sql_query("SELECT * FROM nice_decisions", conn)
nice_df.to_csv("data/processed/nice_decisions.csv", index=False)

conn.close()
print("Exported 3 CSVs to data/processed/")