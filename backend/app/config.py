from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OTO_", extra="ignore")

    app_name: str = "oto-backend"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    default_ticker: str = "AAPL"


@lru_cache
def get_settings() -> Settings:
    return Settings()
