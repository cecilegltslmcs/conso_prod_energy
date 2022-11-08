from airflow.decorators import dag, task
from datetime import datetime
from packages.module_ingestion import *
from packages import authentification as auth
import warnings


if __name__ == "__main__":
  
  warnings.simplefilter("ignore")
  user = auth.user
  password = auth.user
  url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json"
  path = "data/raw/data.json"
  
  @dag(schedule_interval = '@monthly', start_date = datetime(2022, 11, 8), catchup=False)
  
  def taskflow():
    @task(task_id="extract")
    def collecting_from_url():
      print("Collecting data in progress...")
      collecting_data(url, path)
    
    @task(task_id="opening")
    def opening_from_json():
      print("Opening data...")
      df = opening_data(path)
      return df
    
    @task(task_id="parsing")
    def parsing_data():
      print("Parsing data...")
      coverage_rate, region = parsing_data(df)
      return coverage_rate, region
    
    @task(task_id="processing") 
    def processing_parsed_data():
      print("Processing data...")
      consumption = processing_data(consumption)
      return consumption
  
    @task(task_id="sending consumption to database")
    def send_consumption_data():
      print("Sending consumption data to database...")
      sending_database(dataset=consumption, name="consumption", user=user, password=password)
      return "Consumption data send to the database"
    
    @task(task_id="sending coverage rate to database")
    def send_coverage_data():
      print("Sending coverage ratedata to database...")
      sending_database(dataset=coverage_rate, name="coverage_rate", user=user, password=password)
      
    
    print("Data Ingestion finished!")
    
  dag = taskflow()
