"""Configuração lida de variáveis de ambiente.

Toda configuração passa por aqui — não use os.environ direto no resto do código.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: Literal["development", "staging", "production"] = "development"
    app_name: str = "projeto-padrao-backend"
    log_level: Literal["debug", "info", "warning", "error"] = "info"

    database_url: str = Field(
        default="postgresql+psycopg://app:app@localhost:5432/app",
        description="DSN SQLAlchemy/psycopg do Postgres.",
    )

    jwt_secret: str = Field(
        default="change-me-via-vault",
        description="Segredo de assinatura JWT — sobrescrever via cofre em prod.",
        min_length=16,
    )
    jwt_algorithm: str = "HS256"
    jwt_access_ttl_minutes: int = 30
    jwt_refresh_ttl_days: int = 7

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    rate_limit_login_per_minute: str = "10/minute"

    audit_log_retention_days: int = 365 * 5
    tech_log_retention_days: int = 90

    otel_exporter_otlp_endpoint: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
