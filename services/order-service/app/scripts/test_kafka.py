from app.kafka.producer import KafkaProducer

producer = KafkaProducer()

producer.publish(
    topic="order.created",
    message={
        "event": "order.created",
        "order_id": "123",
        "customer_id": "456",
    },
)

print("Event Published!")