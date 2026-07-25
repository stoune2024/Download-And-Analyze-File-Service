from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    external_api_url: str

    candidate_id: str | None = None

    request_timeout: int = 30
    max_retries: int = 5

    database_url: str

    storage_path: str = "storage"

    page_size: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
