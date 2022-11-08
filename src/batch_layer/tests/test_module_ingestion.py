from packages.module_ingestion import *
import pandas as pd
import pytest

def test_collecting_data():
  r = requests.get(f'url')
  assert r.status_code == 200

def test_opening_data():
  df = opening_data(path)
  assert df == type(pd.DataFrame)

def test_parsing_data():
  output1, output2, output3 = parsing_data(df)
  assert output1, output2, output3 == type(pd.DataFrame)

def test_processing_data():
  output1 = processing_data(df)
  assert output1 == type(pd.DataFrame)
  
def test_sending_to_database():
  output1 = sending_to_database()
  assert output1 == "Transfert(s) finished!"

  
