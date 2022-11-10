import requests
from kafka import KafkaProducer
import json

def get_data(url):
    resp = requests.get(url)
    data = resp.json()
    return data

def get_producer(ip_server):
    print("connecting to", ip_server)
    producer = KafkaProducer(
                bootstrap_servers = ip_server,
                value_serializer = lambda x: json.dumps(x).encode('utf-8'))
    return producer

def send_records_to_kafka(producer, topic, records):
    for record in records:
        print("sending records")
        producer.send(topic, record)
