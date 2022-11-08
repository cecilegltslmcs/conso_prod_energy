from packages.module_ingestion import *
import pandas as pd
import pytest

@pytest.fixtures(scope = "module")
def url_data():
  url=""
  return url

@pytest.fixtures(scope = "module")
def data_json():
  json = ""
  return json

@pytest.fixtures(scope = "module")
def df_python():
  df = pd.DataFrame()
  return df

@pytest.fixtures(scope = "module")
def energy_consumption():
  df = pd.DataFrame()
  return df

def test_collecting_data():
  r = requests.get(url_data())
  assert r.status_code == 200

def test_opening_data():
  df = opening_data(data_json())
  assert df == type(pd.DataFrame)

def test_parsing_data():
  output1, output2, output3 = parsing_data(df_python())
  assert output1, output2, output3 == type(pd.DataFrame)

def test_processing_data():
  output1 = processing_data(energy_consumption)
  assert output1 == type(pd.DataFrame)
  
def test_sending_to_database():
  output1 = sending_to_database(energy_consumption, energy, user=user(), password=password())
  assert output1 == "Transfert(s) finished!"

  
