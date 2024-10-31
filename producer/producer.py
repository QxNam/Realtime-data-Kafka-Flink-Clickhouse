from kafka import KafkaProducer
import json
import time
import random

KAFKA_TOPIC = "product_dim"
KAFKA_BOOTSTRAP_SERVERS = "kafka1:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data():
    while True:
        # id, name, slug_name, description, category
        data = {
            "id": random.randint(0, 200),
            "name": random.choice(["view", "click", "purchase", "add_to_cart"]),
            "slug_name": random.choice(["view", "click", "purchase", "add_to_cart"]),
            "description": random.choice(["view", "click", "purchase", "add_to_cart"]),
            "category": random.choice(["view", "click", "purchase", "add_to_cart"]),
            "version": 1
        }
        producer.send(KAFKA_TOPIC, value=data)
        print(f"Data sent: {data}")
        time.sleep(2)

if __name__ == "__main__":
    generate_data()