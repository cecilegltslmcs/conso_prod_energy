# -*- coding: utf-8 -*-
"""This module contained the different functions to collect, open, clean, 
organize and send data to a PostgreSQL. 

"""

import authentification as auth
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import warnings

def collecting_data(url : str):
  """Function which sending requests to 
  the API Odré.
  Return is a json file storage on
  the hard disk.
  
  Parameters
  ------
  url : str
       A string corresponding to the url of the API to requests.
  
  Returns
  ------
  json
      Json File with the information coming from the API.
  
  """
  try:
    response = requests.get(url)
    data = response.json()
  except:
    print('Wrong URL')
  with open('data/energy_data.json', 'w') as f:
    json.dump(data, f)
    return data

def opening_data(path: str):
  """ Function which open the data obtained from the API.
  Three columns are removed in order to realize a first cleaning.
  Return is a Pandas Dataframe. 
  
  Parameters
  ------
  path : str
      Path where the data are stored. 
  Return
  -----
  Pandas Dataframe with the data coming from the API
  """
  df = pd.read_json(path)
  df.drop(["date_heure", "nature", "column_30"], axis=1, inplace=True)
  return df

def cleaning_data(df):
  """
  """
  consumption = df[["code_insee_region", "date", "heure", "consommation",
                  "thermique", "nucleaire", "eolien", "solaire", 
                  "hydraulique", "pompage", "bioenergies"]]
  energy_type = ["thermique", "nucleaire", "eolien", "solaire", 
               "hydraulique", "pompage", "bioenergies"]
  consumption["production_total"] = df["thermique"] + df["nucleaire"] + df["eolien"] +
                                    df["solaire"] + df["hydraulique"] + df["pompage"] +
                                    df["bioenergies"]
  for i in energy_type:
    consumption["pct_"+str(i)] = round((consumption[i]/consumption["production_total"]) * 100, 2)
  
  coverage_rate = df[["code_insee_region", "date", "heure", "tco_thermique",
                    "tch_thermique", "tco_nucleaire", "tch_nucleaire",
                    "tco_eolien", "tch_eolien", "tco_solaire", "tch_solaire",
                    "tco_hydraulique", "tch_hydraulique", "tco_bioenergies",
                    "tch_bioenergies"]]
  
  region = df[["code_insee_region", "libelle_region"]]
  region.drop_duplicates(inplace=True)

  return consumption, coverage_rate, region

def sending_database(dataset, name):
  user = auth.user
  password = auth.password
  engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/energy_consumption')
  engine.connect()
  dataset.to_sql(name=name, con=engine, index=False, if_exists="replace")
