import pandas as pd

CSV_PATH = "data/raw/scmd_final_202503.csv"

df = pd.read_csv(CSV_PATH)

print("=== Shape ===")
print(df.shape)

print("\n=== Columns ===")
print(df.columns.tolist())

print("\n=== First 3 rows ===")
print(df.head(3))

print("\n=== Null counts ===")
print(df.isnull().sum())

print("\n=== Adalimumab rows ===")
mask = df.apply(lambda col: col.astype(str).str.lower().str.contains('adalimumab', na=False)).any(axis=1)
ada_df = df[mask]
print(f"Found {len(ada_df)} rows")
print(ada_df.head(5))