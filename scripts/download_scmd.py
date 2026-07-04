import requests
import os

MONTHS = {
    "202501": "5cde935b-17b6-4c6e-a2a5-bb40d0270288",
    "202502": "b416af4e-fbb4-4bdf-92dc-a784947393ec",
    "202412": "5f834d0c-88c8-4546-a9e5-06ffbe9dd6a2",
    "202411": "1a3fa595-e183-45a7-a3db-7e1c3c941fbc",
    "202410": "88763d12-f7cb-4f61-8f69-770c9493ddde",
    "202409": "11c48b38-ef57-4ddb-93cc-0d59610ead1d",
}

BASE_URL = "https://opendata.nhsbsa.net/dataset/b63be82b-8764-484a-82a1-155b050586da/resource/{resource_id}/download/scmd_final_{month}.csv"

os.makedirs("data/raw", exist_ok=True)

def download_with_retry(url, path, retries=3):
    for attempt in range(retries):
        try:
            print(f"  Attempt {attempt + 1}...")
            r = requests.get(url, verify=False, stream=True, timeout=120)
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"  Failed: {e}")
            if os.path.exists(path):
                os.remove(path)  # 불완전한 파일 삭제
    return False

for month, resource_id in MONTHS.items():
    path = f"data/raw/scmd_final_{month}.csv"
    if os.path.exists(path):
        print(f"Already exists: {month}")
        continue
    url = BASE_URL.format(resource_id=resource_id, month=month)
    print(f"Downloading {month}...")
    success = download_with_retry(url, path)
    if success:
        print(f"Done: {path}")
    else:
        print(f"FAILED after retries: {month}")
        exit(1)

print("All downloads complete.")