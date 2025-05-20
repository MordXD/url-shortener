from app.services.shortener import ShortenerService
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock

@pytest.fixture
def redis_mock():
    redis_client = AsyncMock()
    redis_client.set = AsyncMock()
    redis_client.get = AsyncMock()
    return redis_client

@pytest.mark.asyncio
async def test_create_short_url(redis_mock):
    shortener = ShortenerService(redis_client=redis_mock)
    short_code = await shortener.create_short_url("https://www.google.com")
    assert len(short_code) == 6
    assert short_code.isalnum()
    redis_mock.set.assert_called_once()

@pytest.mark.asyncio
async def test_get_original_url(redis_mock):
    redis_mock.get.return_value = "https://www.google.com"
    shortener = ShortenerService(redis_client=redis_mock)
    original_url = await shortener.get_original_url("abc123")
    assert original_url == "https://www.google.com"
    redis_mock.get.assert_called_once_with("abc123")
    
@pytest.mark.asyncio
async def test_get_original_url_not_found(redis_mock):
    redis_mock.get.return_value = None
    shortener = ShortenerService(redis_client=redis_mock)
    original_url = await shortener.get_original_url("nonexistent")
    assert original_url is None
    redis_mock.get.assert_called_once_with("nonexistent")
    
    