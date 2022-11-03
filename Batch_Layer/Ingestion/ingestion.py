import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import warnings

def collecting_data(url):
  try:
    response = requests.get(url)
    data = response.json()
  except:
    print('Wrong URL')
  with open('data/energy_data.json', 'w') as f:
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
  region.drop_duplicates(inplace=True)

  return consumption, coverage_rate, region

def sending_database(dataset, name):
  user = "postgres"
  password = "password42!"
  engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/energy_consumption')
  engine.connect()
  dataset.to_sql(name=name, con=engine, index=False, if_exists="replace")

if __name__ == "__main__":
  warnings.simplefilter("ignore")
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  path = "data/energy_data.json"

  print("Collecting data in progress...")
  collecting_data(url)
  print("Data obtained!")

  print("Opening data...")
  df = opening_data(path)

  print("Processing data...")
  consumption, coverage_rate, region = cleaning_data(df)
  
  print("Sending data to database...")
  sending_database(consumption, "consumption")
  sending_database(coverage_rate, "coverage_rate")
  sending_database(region, "region")
  
  print("Data Ingestion finished!")