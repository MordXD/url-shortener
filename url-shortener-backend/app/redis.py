from redis.asyncio import Redis
from .core.config import settings





class RedisClient:
    def __init__(self):
        self.redis = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
        try:
            self.redis.ping()
        except Exception as e:
            raise e

    async def close(self):
        await self.redis.close()
