import requests
from yaml import safe_load
from rich import print

requests.packages.urllib3.disable_warnings()

device = {
  "host": "reg01-pro1-rtr.cath.net",
  "port": "443",
  "user": "cathy",
  "password": "lkaoqplcmznauoxkcnxuqyskc",
}

headers = {
  "Accept": "application/yang-data+json",
  "Content-Type": "application/yang-data+json"

}

url = f"https://{device['host']}:{device['host']}/restconf/data/native/interface"

with open("loopback.yml","r") as f:
  loopback_config = safe_load(f)

response = requests.post(url=url, headers=headers, auth=(device['user'], device['password']), json=loopback_config, verify=False)

response.raise_for_status()
if response.ok:
  print("[green]SUCCESS:[/green] {response.status_code}")
