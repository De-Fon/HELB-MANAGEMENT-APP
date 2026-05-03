from functools import wraps
from typing import Callable
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

def idempotent(header_key: str = "Idempotency-Key"):
    """
    Decorator to enforce idempotency. 
    Routes must accept 'request: Request', 'db: Session', and 'service: RequestControlService'.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            db: Session = kwargs.get("db")
            service: RequestControlService = kwargs.get("service")

            if not all([request, db, service]):
                raise RuntimeError("Idempotent route missing required dependencies (request, db, service)")

            idempotency_key = request.headers.get(header_key)
            if not idempotency_key:
                return await func(*args, **kwargs)

            user_id = 1  # TODO: Extract from authenticated user context
            endpoint = service.resolve_endpoint_id(request.method, request.url.path)

            # Check cache
            cached = service.get_cached_response(db, idempotency_key, user_id, endpoint)
            if cached:
                response_body, status_code = cached
                return response_body

            # Execute and store
            result = await func(*args, **kwargs)
            service.store_idempotent_response(db, idempotency_key, user_id, endpoint, 200, result)
            
            return result
        return wrapper
    return decorator

def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    """
    FastAPI Dependency for rate limiting.
    Usage: Depends(rate_limit(10, 60))
    """
    async def dependency(
        request: Request,
        db: Session = Depends(get_db),
        service: RequestControlService = Depends(get_request_control_service)
    ):
        user_id = 1  # TODO: Extract from authenticated user
        endpoint = service.resolve_endpoint_id(request.method, request.url.path)
        
        retry_after = service.validate_rate_limit(
            db, user_id, endpoint, max_requests, window_seconds
        )
        
        if retry_after is not None:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)}
            )
        return True

    return dependency
