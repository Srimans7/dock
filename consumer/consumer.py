from confluent_kafka import Consumer
import requests
import json
import os

# Environment variables
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
MIXTRAL_API_URL = os.getenv('MIXTRAL_API_URL')

consumer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'mixtral-api-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe(['kafka_topic'])

def send_to_mixtral(payload):
    headers = {"Authorization": "Bearer 1yoPmmDpwXNT87ojL47Hjxaj3GkbtbFM", "Content-Type": "application/json"}
    response = requests.post(MIXTRAL_API_URL, payload, headers=headers) 
    return response.json()

print("🚀 Kafka Consumer is listening for messages...")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"❌ Kafka error: {msg.error()}")
        continue

    
    payload = {
    "model": 'mistral-medium',
    "messages": [{"role": "user", "content": msg.value().decode('utf-8')}],
    "temperature": 0.7,
    "max_tokens": 2000
    }

      
    response = send_to_mixtral(payload)
    print(f"✅ Sent: {payload}, Response: {response}")

consumer.close()




curl -X POST -H "Content-Type: application/json" --data '{
  "name": "debezium-postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "localhost",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "password",
    "database.dbname": "n8n",
    "database.server.name": "dbserver1",
    "plugin.name": "pgoutput",
    "table.include.list": "public.booklet",
    "slot.name": "debezium_slot",
    "publication.name": "debezium_publication"
  }
}' http://localhost:8083/connectors

