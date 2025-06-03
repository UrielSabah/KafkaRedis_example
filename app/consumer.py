from confluent_kafka import Consumer
import json

def consume_events(topic: str, config, max_messages=1):
    config["group.id"] = "ad-consumer-group"
    config["auto.offset.reset"] = "earliest"

    consumer = Consumer(config)
    consumer.subscribe([topic])

    messages = []
    try:
        for _ in range(max_messages):
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                key = msg.key().decode("utf-8")
                value = json.loads(msg.value().decode("utf-8"))
                messages.append({"key": key, "event": value})


    finally:
        consumer.close()

    return messages
