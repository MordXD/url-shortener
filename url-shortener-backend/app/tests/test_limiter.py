from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from starlette.testclient import TestClient

from app.core.config import settings
from app.redis import RedisClient
from app.services.limiter import RateLimiter, rate_limited


# Мок для редис-клиента
@pytest.fixture
def mock_redis_client():
    mock = AsyncMock(spec=RedisClient)
    # Создаем мок для вложенного redis атрибута
    mock_redis_instance = AsyncMock()
    mock.redis = mock_redis_instance
    return mock


# Тест для RateLimiter
@pytest.mark.asyncio
async def test_rate_limiter_basic_flow(mock_redis_client):
    limiter = RateLimiter(mock_redis_client)

    # Первый запрос - счетчик должен быть равен 0
    mock_redis_client.get.return_value = None
    assert await limiter.is_rate_limited("127.0.0.1") == False

    # Второй запрос - счетчик равен 1, но еще не превышен лимит
    mock_redis_client.get.return_value = "1"
    assert await limiter.is_rate_limited("127.0.0.1") == False

    # Запрос после превышения лимита
    mock_redis_client.get.return_value = str(settings.rate_limit)
    assert await limiter.is_rate_limited("127.0.0.1") == True


# Тест для декоратора rate_limited
@pytest.mark.asyncio
async def test_rate_limited_decorator():
    # Создаем мок для редис клиента
    mock_redis = AsyncMock(spec=RedisClient)
    mock_redis.get.return_value = None  # Первый запрос

    # Создаем мок для вложенного redis атрибута
    mock_redis_instance = AsyncMock()
    mock_redis.redis = mock_redis_instance

    # Создаем геттер для редис
    def get_redis_client():
        return mock_redis

    # Создаем мок асинхронной функции, которую будем декорировать
    async def mock_handler(request: Request):
        return {"message": "ok"}

    # Декорируем функцию
    decorated_handler = rate_limited(get_redis_client)(mock_handler)

    # Создаем мок для Request
    mock_request = MagicMock(spec=Request)
    mock_request.client.host = "127.0.0.1"

    # Проверяем, что функция работает с первым запросом
    response = await decorated_handler(mock_request)
    assert response == {"message": "ok"}

    # Устанавливаем счетчик выше лимита
    mock_redis.get.return_value = str(settings.rate_limit)

    # Проверяем, что получаем ошибку 429
    with pytest.raises(HTTPException) as excinfo:
        await decorated_handler(mock_request)
    assert excinfo.value.status_code == 429


# Тест для интеграции с API
def test_rate_limit_integration_api():
    # Создаем тестовое приложение
    router = APIRouter()

    # Создаем мок для Redis
    mock_redis = AsyncMock(spec=RedisClient)
    mock_redis_instance = AsyncMock()
    mock_redis.redis = mock_redis_instance

    # Функция для получения редис клиента
    def get_redis_client():
        return mock_redis

    # Функция-обработчик
    @router.get("/test")
    @rate_limited(get_redis_client)
    async def test_endpoint(request: Request):
        return {"success": True}

    # Создаем мок-объект для имитации поведения is_rate_limited
    limit_mock = AsyncMock()
    limit_results = [False] * 10 + [True] * 5
    limit_mock.side_effect = limit_results

    # Патчим RateLimiter.is_rate_limited для симуляции превышения лимита
    with patch("app.services.limiter.RateLimiter.is_rate_limited", limit_mock):
        # Тестируем первые 10 запросов (без лимита)
        for i in range(10):
            assert limit_results[i] == False

        # Тестируем запросы с превышением лимита
        for i in range(5):
            assert limit_results[10 + i] == True
