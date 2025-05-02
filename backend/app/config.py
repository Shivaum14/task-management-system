from functools import lru_cache

from pydantic import PostgresDsn, SecretStr, computed_field
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

    PG_USER: str
    PG_PASSWORD: SecretStr
    PG_HOST: str
    PG_PORT: int
    PG_DB_NAME: str

    @computed_field
    def DB_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.PG_USER,
            password=self.PG_PASSWORD.get_secret_value(),
            host=self.PG_HOST,
            port=self.PG_PORT,
            path=self.PG_DB_NAME,
        )

    class Config:
        env_file = ".env"
        extra = "ignore"
        env_prefix = "APP_"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
