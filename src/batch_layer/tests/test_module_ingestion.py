from packages.module_ingestion import *
import pandas as pd
import pytest

@pytest.fixture()
def url_data():
  url="https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  return url

@pytest.fixture()
def data_json():
  json = "data/raw/data.json"
  return json

@pytest.fixture()
def df_python():
  df = pd.DataFrame()
  return df

@pytest.fixture()
def energy_consumption():
  df = pd.DataFrame()
  return df

@pytest.fixture()
def energy_var():
  energy = energy_var
  return energy

@pytest.fixture()
def user_var():
  user = user_var
  return user

@pytest.fixture()
def password_var():
  password = password_var
  return password

def test_collecting_data():
  r = requests.get(url_data())
  assert r.status_code == 200

def test_opening_data():
  df = opening_data(data_json())
  assert df == type(pd.DataFrame)

def test_parsing_data():
  output1, output2, output3 = parsing_data(df_python())
  assert output1 == type(pd.DataFrame)
  assert output2 == type(pd.DataFrame)
  assert output3 == type(pd.DataFrame)

def test_processing_data():
  output1 = processing_data(energy_consumption())
  assert output1 == type(pd.DataFrame)
  
def test_sending_to_database():
  output1 = sending_database(energy_consumption, energy_var(), user_var(), password_var())
  assert output1 == "Transfert(s) finished!"

  
