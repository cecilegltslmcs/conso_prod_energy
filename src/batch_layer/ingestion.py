from packages.module_ingestion import *
from packages import authentification as auth
import warnings

if __name__ == "__main__":
  warnings.simplefilter("ignore")
  
  user = auth.user
  password = auth.user
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  path = "data/raw"

  print("Collecting data in progress...")
  collecting_data(url, path)

  print("Opening data...")
  df = opening_data(path)

  print("Processing data...")
  consumption, coverage_rate, region = cleaning_data(df)
  
  print("Sending data to database...")
  sending_database(consumption, "consumption", user, password)
  sending_database(coverage_rate, "coverage_rate", user, password)
  sending_database(region, "region", user, password)
  
  print("Data Ingestion finished!")