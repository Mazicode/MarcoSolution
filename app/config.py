from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "redis"  # Using the Docker Compose service name
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0


settings = Settings()
