from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend"
    
    # Database
    DATABASE_URL: str
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis (Celery & Rate Limiting)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_RATE_LIMIT_URL: str = "redis://localhost:6379/1"  # Separate DB for rate limiting
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "200/minute"
    RATE_LIMIT_KEY_PREFIX: str = "helb-rate-limit"
    RATE_LIMIT_REDIS_SOCKET_TIMEOUT_SECONDS: float = 1.0
    RATE_LIMIT_REDIS_CONNECT_TIMEOUT_SECONDS: float = 1.0
    RATE_LIMIT_IN_MEMORY_FALLBACK_ENABLED: bool = True
    RATE_LIMIT_SWALLOW_ERRORS: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
