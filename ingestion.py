import requests
import json

def gathering_data(url):
  response = requests.get(url)
  data = response.json()
  with open('data/data.json', 'w') as f:
    json.dump(data, f)

if __name__ == "__main__":
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  gathering_data(url)