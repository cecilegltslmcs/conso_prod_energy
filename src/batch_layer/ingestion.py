from packages.module_ingestion import *
from streaming_layer.packages import authentification as auth
import warnings


if __name__ == "__main__":
  
  warnings.simplefilter("ignore")
  user = auth.user
  password = auth.password
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  path = "data/raw/data.json"

  print("Collecting data in progress...")
  collecting_data(url, path)

  print("Opening data...")
  df = opening_data(path)

  print("Parsing data data...")
  coverage_rate, region = parsing_data(df)
  
  print("Processing data...")
  consumption = processing_data(df)
  
  print("Sending data to database...")
  sending_database(dataset=consumption, name="consumption", user=user, password=password)
  sending_database(dataset=coverage_rate, name="coverage_rate", user=user, password=password)
  sending_database(dataset=region, name="region", user=user, password=password)
  
  print("Data Ingestion finished!")
