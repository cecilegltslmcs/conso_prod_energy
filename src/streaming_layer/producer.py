from packages.module_kafka import *

if __name__ == "__main__":
    ip = "kafka:9092"
    url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-tr/exports/json"
    producer = get_producer(ip)
    topic = "electricity_production"

    while True:
        data = get_data(url)
        send_records_to_kafka(producer, topic, data)
        print("waiting 1 minute for next records")
        time.sleep(60)
