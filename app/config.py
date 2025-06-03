# app/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import redis.asyncio as redis

load_dotenv()

class Settings(BaseSettings):
    redis_url: str
    kafka_bootstrap_servers: str
    kafka_security_protocol: str
    kafka_sasl_mechanism: str
    kafka_sasl_username: str
    kafka_sasl_password: str
    kafka_topic: str
    kafka_session_timeout_ms: int = 45000
    kafka_client_id: str

    class Config:
        env_file = ".env"


settings = Settings()


redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

def load_kafka_config():
    config = {
        'bootstrap.servers': settings.kafka_bootstrap_servers,
        'security.protocol': settings.kafka_security_protocol,
        'sasl.mechanism': settings.kafka_sasl_mechanism,
        'sasl.username': settings.kafka_sasl_username,
        'sasl.password': settings.kafka_sasl_password,
        'client.id': settings.kafka_client_id
    }
    return config

async def init_redis():
    await redis_client.ping()

async def close_redis():
    await redis_client.close()
