"""
SlowAPI + Redis-backed rate limiting for the HELB backend.

Uses Redis as storage backend for high-performance distributed rate limiting.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.settings import settings

# Initialize SlowAPI Limiter with Redis backend
# Uses Remote Address as the key function (IP-based rate limiting by default)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.REDIS_RATE_LIMIT_URL,
    storage_options={
        "socket_timeout": settings.RATE_LIMIT_REDIS_SOCKET_TIMEOUT_SECONDS,
        "socket_connect_timeout": settings.RATE_LIMIT_REDIS_CONNECT_TIMEOUT_SECONDS,
    },
    default_limits=[settings.RATE_LIMIT_DEFAULT],
    in_memory_fallback=[settings.RATE_LIMIT_DEFAULT],
    in_memory_fallback_enabled=settings.RATE_LIMIT_IN_MEMORY_FALLBACK_ENABLED,
    swallow_errors=settings.RATE_LIMIT_SWALLOW_ERRORS,
    key_prefix=settings.RATE_LIMIT_KEY_PREFIX,
    headers_enabled=True,  # Include X-RateLimit-* headers in response
    enabled=settings.RATE_LIMIT_ENABLED,
)


def setup_rate_limit_exception_handler(app):
    """
    Register the SlowAPI rate limit exception handler.
    Called from main.py to handle 429 responses.
    """
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
        """
        Handle RateLimitExceeded exceptions with structured JSON response.
        """
        logger.warning(
            f"[429] Rate limit exceeded — {request.method} {request.url.path} "
            f"[client={request.client.host if request.client else 'unknown'}]"
        )
        return JSONResponse(
            status_code=429,
            content={
                "error": True,
                "message": "Rate limit exceeded. Please try again later.",
                "detail": str(exc.detail)
            },
        )
