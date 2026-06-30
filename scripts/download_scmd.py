import requests
import os

BASE_URL = "https://opendata.nhsbsa.net/dataset/b63be82b-8764-484a-82a1-155b050586da/resource/{resource_id}/download/scmd_final_{month}.csv"

# 실제 resource ID 매핑 (페이지에서 확인한 것)
MONTHS = {
    "202501": "5cde935b-17b6-4c6e-a2a5-bb40d0270288",
    "202502": "b416af4e-fbb4-4bdf-92dc-a784947393ec",
    "202412": "5f834d0c-88c8-4546-a9e5-06ffbe9dd6a2",
    "202411": "1a3fa595-e183-45a7-a3db-7e1c3c941fbc",
    "202410": "88763d12-f7cb-4f61-8f69-770c9493ddde",
    "202409": "11c48b38-ef57-4ddb-93cc-0d59610ead1d",
}

os.makedirs("data/raw", exist_ok=True)

for month, resource_id in MONTHS.items():
    path = f"data/raw/scmd_final_{month}.csv"
    if os.path.exists(path):
        print(f"Already exists: {month}")
        continue
    url = BASE_URL.format(resource_id=resource_id, month=month)
    print(f"Downloading {month}...")
    r = requests.get(url, verify=False)
    with open(path, 'wb') as f:
        f.write(r.content)
    print(f"Done: {path}")

print("All downloads complete.")