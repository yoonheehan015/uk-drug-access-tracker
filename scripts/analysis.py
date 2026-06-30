import sqlite3
import pandas as pd

conn = sqlite3.connect("db/drug_access.db")

df = pd.read_sql_query("""
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

print("=== Adalimumab 월별 트렌드 ===")
print(df.to_string())

conn.close()