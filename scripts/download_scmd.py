import requests
import os
from datetime import datetime, timedelta

def get_last_month():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime("%Y%m")

def get_resource_id(month_str):
    """NHSBSA API에서 resource ID 자동 조회"""
    dataset_id = "b63be82b-8764-484a-82a1-155b050586da"
    url = f"https://opendata.nhsbsa.net/api/3/action/package_show?id={dataset_id}"
    r = requests.get(url)
    resources = r.json()["result"]["resources"]
    for res in resources:
        if month_str in res.get("name", "") or month_str in res.get("url", ""):
            return res["id"]
    return None

os.makedirs("data/raw", exist_ok=True)

month = get_last_month()
path = f"data/raw/scmd_final_{month}.csv"

if os.path.exists(path):
    print(f"Already exists: {month}")
else:
    resource_id = get_resource_id(month)
    if not resource_id:
        print(f"Resource ID not found for {month}")
        exit(1)
    url = f"https://opendata.nhsbsa.net/dataset/{dataset_id}/resource/{resource_id}/download/scmd_final_{month}.csv"
    print(f"Downloading {month}...")
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
    print(f"Done: {path}")

print("Download complete.")