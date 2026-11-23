import os, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()
token = os.getenv('FORTIGATE_TOKEN')
print(repr(token), len(token))
BASE_URL = f"https://{os.getenv('FORTIGATE_HOST')}/api/v2/cmdb"
HEADERS = {"Authorization": f"Bearer {os.getenv('FORTIGATE_TOKEN')}"}

resp = requests.get(f"{BASE_URL}/firewall/address", headers=HEADERS, verify=False, timeout=5)
resp.raise_for_status()
print(resp.json())