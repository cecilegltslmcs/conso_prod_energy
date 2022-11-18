# -*- coding: utf-8 -*-
"""This module contained the different functions to collect, open, clean, 
organize and send data to a PostgreSQL. 
"""
import requests
import pandas as pd
from sqlalchemy import create_engine

def collecting_data(url : str):
  response = requests.get(url)
  data = response.json()
  df = pd.read_json(data)
  df.drop(["date_heure", "nature", "column_30"], axis=1, inplace=True)
  
  return df

def parsing_data(df):
  coverage_rate = df[["code_insee_region", "date", "heure", "tco_thermique",
                    "tch_thermique", "tco_nucleaire", "tch_nucleaire",
                    "tco_eolien", "tch_eolien", "tco_solaire", "tch_solaire",
                    "tco_hydraulique", "tch_hydraulique", "tco_bioenergies",
                    "tch_bioenergies"]]
  coverage_rate.fillna(0, inplace=True)
  
  region = df[["code_insee_region", "libelle_region"]]
  region.drop_duplicates(inplace=True)
  
  return coverage_rate, region

def processing_data(df):
  consumption = df[["code_insee_region", "date", "heure", "consommation",
                  "thermique", "nucleaire", "eolien", "solaire", 
                  "hydraulique", "pompage", "bioenergies"]]
  consumption.fillna(0, inplace=True)
  consumption["production_total"] = consumption["thermique"] + consumption["nucleaire"] + consumption["eolien"] +\
                           consumption["solaire"] + consumption["hydraulique"] + consumption["pompage"] +\
                           consumption["bioenergies"]
  energy_type = ["thermique", "nucleaire", "eolien", "solaire", 
                 "hydraulique", "pompage", "bioenergies"]
  for i in energy_type:
    consumption["pct_" + str(i)] = round((consumption[i]/consumption["production_total"]) * 100, 2)
    
  return consumption

def sending_database(db_user, db_password, dataset, table_name):
  engine = create_engine(f'postgresql://{db_user}:{db_password}@database:5432/energy_consumption')
  engine.connect()

  dataset.to_sql(name=table_name, con=engine, if_exists="append")
  
  return f"{dataset} insert  in database"