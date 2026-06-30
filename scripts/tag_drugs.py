import sqlite3

conn = sqlite3.connect("db/drug_access.db")
cur = conn.cursor()

# 아달리무맙 → biosimilar / rheumatology 태깅
cur.execute("""
UPDATE drugs
SET access_route = 'biosimilar',
    therapy_area = 'rheumatology'
WHERE LOWER(vmp_product_name) LIKE '%adalimumab%'
""")

print(f"Tagged {cur.rowcount} adalimumab drugs.")
conn.commit()

# 확인
cur.execute("""
SELECT vmp_product_name, access_route, therapy_area
FROM drugs
WHERE access_route IS NOT NULL
""")
for row in cur.fetchall():
    print(row)

conn.close()