from ingestion import *
import pandas as pd
import pytest

def test_collecting_data():
  output = collecting_data(url)
  assert output == "Data collected from API successfully."
  
def test_opening_data():
  output = opening_data(path)
  assert output == type(json)

def test_cleaning_data():
  output1, output2, output3 = cleaning_data(data)
  assert output1, output2, output3 == type(pd.dataframe)

def test_sending_database():
  output = sending_database()
  assert output == "Transfer.s finished!"
  
