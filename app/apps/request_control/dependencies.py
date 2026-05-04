from functools import wraps
from typing import Callable, Any
from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService
import asyncio

def idempotent(header_key: str = "Idempotency-Key"):
    """Decorator to enforce idempotency. Handles both sync and async route handlers."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            db: Session = kwargs.get("db")
            
            # Look for rc_service or service (if it's the right type)
            service = kwargs.get("rc_service")
            if not service:
                potential_service = kwargs.get("service")
                if isinstance(potential_service, RequestControlService):
                    service = potential_service

            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not all([request, db, service]):
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)

            idempotency_key = request.headers.get(header_key)
            if not idempotency_key:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)

            user_id = 1 # Placeholder
            endpoint = service.resolve_endpoint_id(request.method, request.url.path)

            cached = service.get_cached_response(db, idempotency_key, user_id, endpoint)
            if cached:
                from loguru import logger
                logger.info(f"Idempotency hit: {request.method} {request.url.path} [Key: {idempotency_key}]")
                # Return the cached response as a proper JSONResponse
                return JSONResponse(content=cached[0], status_code=cached[1])

            # Execute the function based on its type
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Determine appropriate status code (default to 200, 201 for POST usually)
            # In a more advanced version, we'd inspect the route's status_code
            status_code = status.HTTP_200_OK
            if request.method == "POST":
                status_code = status.HTTP_201_CREATED
                
            service.store_idempotent_response(db, idempotency_key, user_id, endpoint, status_code, result)
            return result
        return wrapper
    return decorator

def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    """Decorator to enforce rate limiting. Handles both sync and async route handlers."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            db: Session = kwargs.get("db")
            
            # Look for rc_service or service (if it's the right type)
            service = kwargs.get("rc_service")
            if not service:
                potential_service = kwargs.get("service")
                if isinstance(potential_service, RequestControlService):
                    service = potential_service

            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not all([request, db, service]):
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)

            user_id = 1 # Placeholder
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
            
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
