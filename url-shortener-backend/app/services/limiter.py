import time
from functools import wraps
from typing import Callable, Optional
from fastapi import HTTPException, Request, status

from app.redis import RedisClient
from app.core.config import settings


class RateLimiter:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client
        self.rate_limit = settings.rate_limit
        self.window = 60  # 1 минута

    async def _get_current_usage(self, key: str) -> int:
        """Получает текущее количество запросов для ключа"""
        count = await self.redis_client.get(key)
        return int(count) if count else 0

    async def is_rate_limited(self, ip: str) -> bool:
        """Проверяет, превышен ли лимит для данного IP"""
        key = f"rate_limit:{ip}"
        current_count = await self._get_current_usage(key)

        if current_count >= self.rate_limit:
            return True

        # Увеличиваем счетчик или устанавливаем его, если не существует
        if current_count == 0:
            await self.redis_client.set(key, "1", ex=self.window)
        else:
            # Обновляем счетчик
            await self.redis_client.redis.incr(key)

        return False


def rate_limited(redis_client_getter: Callable[[], RedisClient]):
    """
    Декоратор для ограничения частоты запросов.
    
    Args:
        redis_client_getter: Функция, возвращающая RedisClient
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Получаем IP-адрес клиента
            client_ip = request.client.host
            redis_client = redis_client_getter()
            limiter = RateLimiter(redis_client)
            
            # Проверяем, не превышен ли лимит
            is_limited = await limiter.is_rate_limited(client_ip)
            if is_limited:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later."
                )
            
            # Если лимит не превышен, выполняем оригинальную функцию
            return await func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
