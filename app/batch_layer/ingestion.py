from packages.module_ingestion import *
from packages import authentification as auth
import warnings


if __name__ == "__main__":
  
  warnings.simplefilter("ignore")
  user = auth.user
  password = auth.password
  host = auth.host
  port = auth.port
  database = auth.database
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  #path = "data/raw/data.json"

  print("Collecting data in progress...")
  df = collecting_data(url)

  # print("Opening data...")
  # df = opening_data(path)

  print("Parsing data...")
  coverage_rate, region = parsing_data(df)
  
  print("Processing data...")
  consumption = processing_data(df)
  
  print("Sending data to database...")
  sending_database(db_user=user, 
                  db_password=password, 
                  localhost=host, 
                  port=port, 
                  database=database,
                   dataset=consumption, 
                   name="consumption")
  sending_database(db_user=user, 
                   db_password=password, 
                   localhost=host, 
                   port=port, 
                   database=database,
                   dataset=coverage_rate, 
                   name="coverage_rate")
  sending_database(db_user=user, 
                   db_password=password, 
                   localhost=host, 
                   port=port, 
                   database=database,  
                   dataset=region, 
                   name="region")
  
  print("Data Ingestion finished!")
