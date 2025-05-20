from fastapi import Depends, FastAPI
import uvicorn
from .redis import RedisClient

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/status")
async def check_redis(redis_client: RedisClient = Depends(RedisClient)):
    return {"status": "ok" if await redis_client.redis.ping() else "error"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)