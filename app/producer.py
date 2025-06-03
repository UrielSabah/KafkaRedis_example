from confluent_kafka import Producer
import json

from app.logger import setup_logger

logger = setup_logger(__name__)


producer = None

def init_producer(config):
    global producer
    if not producer:
        producer = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        logger.info(f"❌ Delivery failed: {err}")
    else:
        logger.info(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

def send_event(topic: str, event: dict):
    value = json.dumps(event)
    key = str(event.get("user_id", "unknown"))
    producer.produce(topic, key=key, value=value, callback=delivery_report)
    producer.flush()
