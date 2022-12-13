from packages.module_kafka import *
import time

if __name__ == "__main__":
    ip = "kafka:9092"
    topic = "electricity_production"
    url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-tr/exports/json"
    producer = get_producer(ip)
    

    while True:
        data = get_data(url)
        send_records_to_kafka(producer, topic, data)
        print("waiting 15 minutes for next records")
        time.sleep(900)
