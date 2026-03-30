from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OTO_", extra="ignore")

    app_name: str = "oto-backend"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    default_ticker: str = "AAPL"
    # SEC requires a descriptive User-Agent with contact (see https://www.sec.gov/os/webmaster-faq)
    sec_user_agent: str = "OTO-Research/0.1 (oto-backend; contact: dev@localhost)"
    # "sec" uses SEC EDGAR CompanyFacts; "mock" uses in-memory sample data (tests/offline).
    research_data_source: str = "sec"


@lru_cache
def get_settings() -> Settings:
    return Settings()
