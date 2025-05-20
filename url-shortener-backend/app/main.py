from fastapi import Depends, FastAPI
import uvicorn
from .redis import RedisClient
from .api import router, get_redis_client

app = FastAPI(title="URL Shortener API")

# Создаем глобальную переменную для Redis клиента
redis_client = None

@app.on_event("startup")
async def startup_db_client():
    """Инициализация подключения к Redis при старте приложения."""
    global redis_client
    redis_client = RedisClient()
    print("Redis connection established")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Закрытие подключения к Redis при остановке приложения."""
    global redis_client
    if redis_client:
        await redis_client.close()
        print("Redis connection closed")

# Определяем эндпоинт статуса перед подключением основного роутера
@app.get("/status")
async def check_redis(redis_client: RedisClient = Depends(get_redis_client)):
    return {"status": "ok" if await redis_client.redis.ping() else "error"}

# Подключаем роутер API к корневому пути
app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)