"""
Application configuration using Pydantic Settings.

Loads from environment variables and .env file.
"""

from functools import lru_cache
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # === Application ===
    APP_NAME: str = "SiteBlitz Lead Intelligence OS"
    APP_VERSION: str = "0.1.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    # === Database ===
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/siteblitz_leads"
    DATABASE_URL_SYNC: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/siteblitz_leads"
    )
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # === Redis ===
    REDIS_URL: str = "redis://localhost:6379/0"

    # === CORS ===
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # === Source API Keys ===
    HUNTER_API_KEY: Optional[str] = None
    GOOGLE_PAGESPEED_API_KEY: Optional[str] = None

    # === Overture Maps Places ===
    # Dated release folder on s3://overturemaps-us-west-2/release/ (monthly). Newest on
    # 2026-11-08 = 2026-10-21.0; old releases are removed, so update this when reads fail.
    # Release notes: https://docs.overturemaps.org/blog
    OVERTURE_RELEASE: str = "2026-10-21.0"

    # === Rate Limits (requests per minute) ===
    OSM_OVERPASS_RPM: int = 10
    WIKIDATA_RPM: int = 30
    DEFAULT_CRAWL_RPM: int = 20

    # === Logging ===
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
