"""
HTTP request logging middleware using Loguru.

Logs every incoming request and its response with:
  - Method, path, query params
  - Response status code
  - Processing duration in milliseconds
  - Client IP address
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs every HTTP request and response."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Build a readable query string if present
        query_string = f"?{request.url.query}" if request.url.query else ""
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            f"→ {request.method} {request.url.path}{query_string} "
            f"[client={client_ip}]"
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                f"✗ {request.method} {request.url.path} "
                f"UNHANDLED EXCEPTION after {duration_ms:.1f}ms — {exc}"
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        status_code = response.status_code

        # Log level based on status code
        if status_code >= 500:
            log_fn = logger.error
        elif status_code >= 400:
            log_fn = logger.warning
        else:
            log_fn = logger.info

        log_fn(
            f"← {request.method} {request.url.path}{query_string} "
            f"[{status_code}] {duration_ms:.1f}ms [client={client_ip}]"
        )

        return response
