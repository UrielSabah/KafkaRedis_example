from fastapi import FastAPI, Request, HTTPException
import asyncio

from contextlib import asynccontextmanager
from app.producer import init_producer, send_event
from app.consumer import consume_events
from app.config import init_redis, close_redis, load_kafka_config, settings
from app.services.user_service import get_user_action
from app.models import Event  # Import the Pydantic model
from app.logger import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await close_redis()


app = FastAPI(lifespan=lifespan)
logger = setup_logger("main")

KAFKA_TOPIC = settings.kafka_topic
KAFKA_CONFIG = load_kafka_config()
init_producer(KAFKA_CONFIG)

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    try:
        #Caching data
        data = await get_user_action(user_id)
        #Publishing to Kafka
        await asyncio.to_thread(send_event, KAFKA_TOPIC, data)
        return {"status": "success", "event": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish to kafka: {e}")


@app.get("/events/consume")
def consume_event():
    try:
        messages = consume_events(topic=KAFKA_TOPIC, config=KAFKA_CONFIG, max_messages=5)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to consume to kafka: {e}")




