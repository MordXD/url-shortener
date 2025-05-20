from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str = "redis"
    redis_port: int = 6379
    base_url: str = "http://localhost"
    rate_limit: int = 10
    redis_url: str = "redis://redis:6379/0"
    ttl: int = 86400

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
