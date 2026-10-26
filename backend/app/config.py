from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="modelops-lab-api")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    database_url: str = Field(
        default="postgresql+psycopg://modelops:modelops@localhost:5432/modelops"
    )
    artifact_storage_path: str = Field(default="storage/artifacts")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
