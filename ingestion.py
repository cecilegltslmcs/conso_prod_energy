import requests
import json

url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
response = requests.get(url)

data = response.json()
with open('data.json', 'w') as f:
  json.dump(data, f)