from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    HOST: str = "127.0.0.1"
    PORT: int = 8010
    RELOAD: bool = True
    WORKERS: int = 1
    LOG_LEVEL: str = "info"
    LOG_CONFIG: str = "app/core/log_configs/log-prod.yml"
    ENVIRONMENT: str = "dev"
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
