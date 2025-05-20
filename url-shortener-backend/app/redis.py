from redis.asyncio import Redis
from .core.config import settings





class RedisClient:
    def __init__(self):
        self.redis = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
    
    async def ping(self):
        return await self.redis.ping()
    
    async def set(self, key: str, value: str, ex: int = None):
        return await self.redis.set(key, value, ex=ex or settings.ttl)
    
    async def get(self, key: str):
        return await self.redis.get(key)
    
    async def delete(self, key: str):
        return await self.redis.delete(key)
    
    async def close(self):
        await self.redis.close()
