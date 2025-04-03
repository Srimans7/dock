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
