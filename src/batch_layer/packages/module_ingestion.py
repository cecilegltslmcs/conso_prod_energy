# -*- coding: utf-8 -*-
"""This module contained the different functions to collect, open, clean, 
organize and send data to a PostgreSQL. 
"""
import requests
import pandas as pd
from sqlalchemy import create_engine

def collecting_data(url : str):
  """Function which sending requests to 
  the API Odre.
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
  
  df = pd.read_json(data)
  df.drop(["date_heure", "nature", "column_30"], axis=1, inplace=True)
  return df

# def opening_data(path: str):
#   """ Function which open the data obtained from the API.
#   Three columns are removed in order to realize a first cleaning.
#   Return is a Pandas Dataframe. 
  
#   Parameters
#   ------
#   path : str
#       Path where the data are stored. 
#   Return
#   -----
#   Pandas Dataframe with the data coming from the API
#   """
#   df = pd.read_json(path)
#   df.drop(["date_heure", "nature", "column_30"], axis=1, inplace=True)
#   return df

def parsing_data(df):
  """This function cleans and preprocesses the data 
  coming from the given dataset. 
  Return three datasets.
  
  Parameters
  ------
  df : dataframe
      Dataframe which need to be cleaned and preprocessed.
  Return
  -----
  Three datasets with the consumption and production information, 
  coverage_rate and region.
  """

  
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
    consumption["pct_"+str(i)] = round((consumption[i]/consumption["production_total"]) * 100, 2)
    
  return consumption

def sending_database(dataset, name, user, password):
  """ Function which connect to the PostgreSQL database
  and send the cleaned-processed data for storage.
  
  Parameters:
  -------
  dataset : dataframe
      Clean dataframe to transfer to the database.
  name : str
      Name of the dataframe to transfer to the database.
  user : str
      User name to establish the connection to PostgreSQL.
  password : str
      Password to identify the user and establish the connection to PostgreSQL.
  
  Return
  -----
  A message to validate the success of the transfert. 
  
  """
  try:
    engine = create_engine(f'postgresql://{user}:{password}@postgres:5432/energy_consumption')
    engine.connect()
  except:
    print("Error while connection to the database")
  dataset.to_sql(name=name, con=engine, index=False, if_exists="replace")
  
  return "Transfert(s) finished!"
