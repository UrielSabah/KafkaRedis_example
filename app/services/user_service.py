# app/services/user_service.py
import json
import asyncio
import random
from app.config import redis_client


async def fetch_from_db(user_id: int) -> dict:
    await asyncio.sleep(0.3)  # simulate DB delay
    return {
        "user_id": user_id,
        "action": "play",
        "context":{
        "movie": random.choice(["Thursday", "Inception", "Matrix"])
        }
    }

async def get_user_action(user_id: int) -> dict:
    cache_key = f"user:{user_id}"
    cached = await redis_client.get(cache_key)

    if cached:
        print("✅ Redis: Cache hit")
        user_data = json.loads(cached)
    else:
        print("📦 Redis: Cache miss → DB fallback")
        user_data = await fetch_from_db(user_id)
        await redis_client.setex(cache_key, 60, json.dumps(user_data))

    return user_data
