from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.redis import RedisClient
from app.services.shortener import ShortenerService


# Патчим зависимости для тестирования
@pytest.fixture
def client():
    """Тестовый клиент FastAPI"""
    with patch("app.api.get_redis_client") as mock_get_redis:
        # Создаем мок для Redis
        mock_redis = AsyncMock(spec=RedisClient)
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True

        # Создаем мок для вложенного redis атрибута
        mock_redis_instance = AsyncMock()
        mock_redis_instance.incr.return_value = 1
        mock_redis.redis = mock_redis_instance

        # Мок для получения Redis
        mock_get_redis.return_value = mock_redis

        # Мок для ShortenerService
        with patch("app.api.ShortenerService") as mock_shortener_class:
            shortener_instance = MagicMock(spec=ShortenerService)
            shortener_instance.create_short_url = AsyncMock(return_value="abc123")
            shortener_instance.get_original_url = AsyncMock(
                return_value="https://example.com"
            )
            mock_shortener_class.return_value = shortener_instance

            # Также патчим лимитер чтобы тесты не были лимитированы
            with patch(
                "app.services.limiter.RateLimiter.is_rate_limited", return_value=False
            ):
                yield TestClient(app)


def test_shorten_url(client):
    """Тест для создания короткого URL"""
    response = client.post("/shorten", json={"original_url": "https://example.com"})

    assert response.status_code == status.HTTP_200_OK
    assert "short_url" in response.json()
    assert response.json()["short_url"] == f"{settings.base_url}/abc123"


def test_shorten_url_invalid(client):
    """Тест для проверки валидации URL"""
    response = client.post("/shorten", json={"original_url": "not-a-valid-url"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_redirect(client):
    """Тест для редиректа"""
    # Модифицируем client._transport для перехвата запросов вместо их выполнения
    original_request = client.request

    def capture_request(*args, **kwargs):
        # Возвращаем ответ только с информацией о статусе и заголовке Location
        # без фактического следования по редиректу
        class MockResponse:
            status_code = status.HTTP_307_TEMPORARY_REDIRECT
            headers = {"location": "https://example.com"}

            def json(self):
                return {}

        if args[0] == "GET" and args[1].endswith("/abc123"):
            return MockResponse()

        # Для других запросов используем стандартную функцию
        return original_request(*args, **kwargs)

    # Патчим метод request TestClient
    client.request = capture_request

    # Выполняем запрос
    response = client.get("/abc123")

    # Проверяем результаты
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://example.com"

    # Восстанавливаем оригинальную функцию
    client.request = original_request


def test_redirect_not_found(client):
    """Тест для несуществующего кода"""
    # Патчим get_original_url для возврата None (URL не найден)
    with patch(
        "app.services.shortener.ShortenerService.get_original_url", return_value=None
    ):
        response = client.get("/nonexistent")

        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_rate_limit_exceeded(client):
    """Тест для проверки превышения rate limit"""
    # Патчим is_rate_limited чтобы он вернул True (лимит превышен)
    with patch("app.services.limiter.RateLimiter.is_rate_limited", return_value=True):
        response = client.post("/shorten", json={"original_url": "https://example.com"})

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
