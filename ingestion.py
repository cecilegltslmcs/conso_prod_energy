import requests
import json

def gathering_data(url):
  try:
    response = requests.get(url)
    data = response.json()
  except:
    print('Wrong URL')
  print("Saving in progress...")
  with open('data/energy_data.json', 'w') as f:
    json.dump(data, f)
  print("Saving termined!")

if __name__ == "__main__":
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  gathering_data(url)