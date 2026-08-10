import json
import os

from confluent_kafka import Consumer


consumer = Consumer(
    {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        "group.id": "order-consumer-group-v2",
        "auto.offset.reset": "earliest",
    }
)

topic = os.getenv("KAFKA_TOPIC")

consumer.subscribe([topic])

print(f"Listening on topic: {topic}")

try:
    while True:
        msg = consumer.poll(timeout=5.0)

        print(msg)

        if msg is None:
            continue

        if msg.error():
            print(msg.error())
            continue

        data = json.loads(msg.value().decode("utf-8"))

        print("\n📦 Order Event Received")
        print(data)

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()