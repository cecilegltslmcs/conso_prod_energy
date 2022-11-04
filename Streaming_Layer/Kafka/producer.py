import requests
import time
from kafka import KafkaProducer
import json

def get_data(url):
    mytime = strftime('%Y-%m-%d %H:%M:%S', localtime())

    resp = requests.get(url)

    data = resp.json()
    data['timestamp'] = mytime

    return data

def get_producer(ip, port=9092):
    broker = f"{ip}:{port}"
    print("connecting to ", broker)

    producer = KafkaProducer(
                bootstrap_servers = [broker],
                value_serializer = lambda x: json.dumps(x).encode('utf-8')
    )

    return producer

def send_records_to_kafka(producer, topic, records):
    for record in records:
        print("sending records")
        producer.send(topic, record)

if __name__ == "__main__":
    ip = "localhost"
    url = "https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-tr/exports/json"
    producer = get_producer(ip)
    topic = "electricity_production"

    while True:
        data = get_data(url)
        send_records_to_kafka(producer, topic, data['records'])
        print("waiting 15 minutes for next records")
        time.sleep(900)