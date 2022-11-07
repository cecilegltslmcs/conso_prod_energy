from ingestion_module import *

if __name__ == "__main__":
  warnings.simplefilter("ignore")
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  path = "data/energy_data.json"

  print("Collecting data in progress...")
  collecting_data(url)
  print("Data obtained!")

  print("Opening data...")
  df = opening_data(path)

  print("Processing data...")
  consumption, coverage_rate, region = cleaning_data(df)
  
  print("Sending data to database...")
  sending_database(consumption, "consumption")
  sending_database(coverage_rate, "coverage_rate")
  sending_database(region, "region")
  
  print("Data Ingestion finished!")
