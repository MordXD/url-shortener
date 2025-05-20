import string
from random import choices
from typing import Optional

from app.redis import RedisClient


class ShortenerService:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def create_short_url(self, original_url: str) -> str:
        short_code = "".join(choices(string.ascii_letters + string.digits, k=6))

        await self.redis_client.set(short_code, original_url)

        return short_code

    async def get_original_url(self, short_code: str) -> Optional[str]:
        original_url = await self.redis_client.get(short_code)
        return original_url if original_url else None
