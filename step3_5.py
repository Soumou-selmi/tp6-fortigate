import os, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

BASE_URL = f"https://{os.getenv('FORTIGATE_HOST')}/api/v2/cmdb"
HEADERS = {"Authorization": f"Bearer {os.getenv('FORTIGATE_TOKEN').strip()}"}

def post(path, payload):
    r = requests.post(f"{BASE_URL}{path}", json=payload, headers=HEADERS, verify=False)
    print(path, r.status_code, r.text)
    r.raise_for_status()

# Étape 3 : objet réseau
post("/firewall/address", {
    "name": "SRV-WEB-01",
    "subnet": "10.0.10.50/32",
})

# Étape 4 : VIP (443 externe -> SRV-WEB-01 en interne)
post("/firewall/vip", {
    "name": "VIP-WEB-HTTPS",
    "extip": "192.168.55.99",
    "extintf": "port1",
    "portforward": "enable",
    "protocol": "tcp",
    "extport": "443",
    "mappedport": "443",
    "mappedip": [{"range": "10.0.10.50"}],
})

# Étape 5 : règle de filtrage vers la VIP
post("/firewall/policy", {
    "name": "ALLOW-WEB-HTTPS",
    "srcintf": [{"name": "port1"}],
    "dstintf": [{"name": "port2"}],
    "srcaddr": [{"name": "all"}],
    "dstaddr": [{"name": "VIP-WEB-HTTPS"}],
    "service": [{"name": "HTTPS"}],
    "schedule": "always",
    "action": "accept",
    "nat": "disable",
    "logtraffic": "all",
})