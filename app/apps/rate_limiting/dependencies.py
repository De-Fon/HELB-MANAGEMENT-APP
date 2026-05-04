from functools import wraps
from typing import Callable
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import asyncio

from app.core.database import get_db
from app.apps.rate_limiting.service import RateLimitService
from app.apps.rate_limiting.providers import get_rate_limit_service

def rate_limit(max_requests: int = 5, window_seconds: int = 60):
    """Decorator to enforce rate limiting."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            db: Session = kwargs.get("db")
            service: RateLimitService = kwargs.get("rate_limit_service")

            # Resolve missing dependencies from args if necessary
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not all([request, db, service]):
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            # Placeholder for user_id
            user_id = 1
            endpoint = f"{request.method} {request.url.path}"

            is_allowed, retry_after = service.check_rate_limit(db, user_id, endpoint, max_requests, window_seconds)
            
            if not is_allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Retry after {retry_after} seconds."
                )

            return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        return wrapper
    return decorator
