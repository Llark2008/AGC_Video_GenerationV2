from typing import AsyncGenerator
import redis.asyncio as aioredis
from .config import get_settings

settings = get_settings()

redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    try:
        yield redis_client
    finally:
        await redis_client.close()
