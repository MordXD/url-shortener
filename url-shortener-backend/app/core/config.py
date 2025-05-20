from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    redis_host: str = "redis"
    redis_port: int = 6379
    base_url: str = "http://localhost:8000"
    rate_limit: int = 10
    

    class Config:
        env_file = ".env"

settings = Settings()