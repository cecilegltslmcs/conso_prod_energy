import requests
import json
import pandas as pd

def collecting_data(url):
  try:
    response = requests.get(url)
    data = response.json()
  except:
    print('Wrong URL')
  with open('data/raw/energy_data.json', 'w') as f:
    json.dump(data, f)

def opening_data(path):
  df = pd.read_json(path)
  df.drop(["date_heure", "nature", "column_30"], axis=1, inplace=True)
  return df

def cleaning_data(df):
  consumption = df[["code_insee_region", "date", "heure", "consommation",
                  "thermique", "nucleaire", "eolien", "solaire", 
                  "hydraulique", "pompage", "bioenergies"]]
  energy_type = ["thermique", "nucleaire", "eolien", "solaire", 
               "hydraulique", "pompage", "bioenergies"]
  for i in energy_type:
    consumption["%_"+str(i)] = round((consumption[i]/consumption["consommation"]) * 100, 2)
  
  coverage_rate = df[["code_insee_region", "date", "heure", "tco_thermique",
                    "tch_thermique", "tco_nucleaire", "tch_nucleaire",
                    "tco_eolien", "tch_eolien", "tco_solaire", "tch_solaire",
                    "tco_hydraulique", "tch_hydraulique", "tco_bioenergies",
                    "tch_bioenergies"]]
  
  region = df[["code_insee_region", "libelle_region"]]

  return consumption, coverage_rate, region

def saving_data(dataset):
  dataset.to_parquet("data/processed"+str(dataset)+".parquet.gzip",
                      compression="gzip")

if __name__ == "__main__":
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  path = "data/raw/energy_data.json"

  print("Collecting data in progress...")
  collecting_data(url)
  print("Data obtained!")

  print("Opening data...")
  df = opening_data(path)

  print("Processing data...")
  consumption, coverage_rate, region = cleaning_data(df)

  print("Saving data...")
  saving_data(consumption)
  saving_data(coverage_rate)
  saving_data(region)
