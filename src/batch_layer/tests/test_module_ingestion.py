from packages.module_ingestion import *
import pandas as pd
import pytest

def test_collecting_data():
  r = requests.get(f'url')
  assert r.status_code == 200

def test_opening_data():
  

  
