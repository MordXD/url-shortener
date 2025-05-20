from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl, BaseModel

from app.core.config import settings
from app.redis import RedisClient
from app.services.limiter import rate_limited
from app.services.shortener import ShortenerService


class URLRequest(BaseModel):
    original_url: AnyUrl


class URLResponse(BaseModel):
    short_url: str


router = APIRouter()


def get_redis_client():
    """Dependency для получения Redis клиента"""
    return RedisClient()


def get_shortener_service(redis_client: RedisClient = Depends(get_redis_client)):
    """Dependency для получения ShortenerService"""
    return ShortenerService(redis_client)


@router.post("/shorten", response_model=URLResponse)
@rate_limited(get_redis_client)
async def shorten_url(
    request: Request,
    url_request: URLRequest,
    shortener_service: ShortenerService = Depends(get_shortener_service),
):
    """Сокращает URL и возвращает короткую версию"""
    short_code = await shortener_service.create_short_url(str(url_request.original_url))
    short_url = f"{settings.base_url}/{short_code}"

    return URLResponse(short_url=short_url)


@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    shortener_service: ShortenerService = Depends(get_shortener_service),
):
    """Редирект на оригинальный URL"""
    # Проверяем длину короткого кода
    if len(short_code) != 6:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    original_url = await shortener_service.get_original_url(short_code)

    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    return RedirectResponse(
        original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
