import requests
import time
from kafka import KafkaProducer
import json

def get_data(url):
    resp = requests.get(url)
    data = resp.json()
    return data

def get_producer(ip, port=9092):
    broker = f"{ip}:{port}"
    print("connecting to", broker)
    producer = KafkaProducer(
                bootstrap_servers = [broker],
                value_serializer = lambda x: json.dumps(x).encode('utf-8'))
    return producer

def send_records_to_kafka(producer, topic, records):
    for record in records:
        print("sending records")
        producer.send(topic, record)
