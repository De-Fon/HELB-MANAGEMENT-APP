from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    PROJECT_NAME: str = "FastAPI Backend"

    # Database
    DATABASE_URL: str

    # Security
    JWT_SECRET: str = Field(validation_alias=AliasChoices("JWT_SECRET", "JWT_SECRET_KEY"))
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SMS
    SMS_API_KEY: str

    # Redis (Celery & Rate Limiting)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_RATE_LIMIT_URL: str = "redis://localhost:6379/1"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "200/minute"
    RATE_LIMIT_KEY_PREFIX: str = "helb-rate-limit"
    RATE_LIMIT_REDIS_SOCKET_TIMEOUT_SECONDS: float = 1.0
    RATE_LIMIT_REDIS_CONNECT_TIMEOUT_SECONDS: float = 1.0
    RATE_LIMIT_IN_MEMORY_FALLBACK_ENABLED: bool = True
    RATE_LIMIT_SWALLOW_ERRORS: bool = False

    @property
    def JWT_SECRET_KEY(self) -> str:
        """Backward-compatible alias for older imports."""
        return self.JWT_SECRET

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance for dependency injection."""
    return Settings()


settings = get_settings()
