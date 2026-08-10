import json
import os

from confluent_kafka import Producer


class KafkaProducer:

    def __init__(self):
        self.producer = Producer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            }
        )

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print(f"❌ Delivery failed: {err}")
        else:
            print(
                f"✅ Delivered to topic={msg.topic()}, "
                f"partition={msg.partition()}, "
                f"offset={msg.offset()}"
            )

    def publish(self, message: dict) -> None:
        topic = os.getenv("KAFKA_TOPIC")

        self.producer.produce(
            topic=topic,
            value=json.dumps(message),
            on_delivery=self.delivery_report,
        )

        self.producer.flush()