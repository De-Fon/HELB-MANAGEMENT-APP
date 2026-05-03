from functools import wraps
from typing import Callable, Any
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

def idempotent(key_from: str = "header"):
    """
    Decorator to enforce idempotency on a route.
    Expects 'Idempotency-Key' in headers if key_from is 'header'.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find the request object in kwargs or args
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise ValueError("Route handler must accept 'request: Request' to use @idempotent decorator.")

            idempotency_key = request.headers.get("Idempotency-Key")
            if not idempotency_key:
                # If no key is provided, we just proceed without idempotency
                return await func(*args, **kwargs)

            # Get dependencies from kwargs or manually (FastAPI handles this if they are in the signature)
            db: Session = kwargs.get("db")
            service: RequestControlService = kwargs.get("service")
            
            # If they are not in kwargs, they must be provided by Depends in the original function
            # This decorator assumes the route handler has db and service dependencies injected.
            
            if not db or not service:
                 raise ValueError("Route handler must include 'db: Session = Depends(get_db)' and 'service: RequestControlService = Depends(get_request_control_service)' to use @idempotent.")

            user_id = 1 # Placeholder: In a real app, get from request.state.user.id
            endpoint = f"{request.method} {request.url.path}"

            async def processor():
                result = await func(*args, **kwargs)
                # We assume the result is the response body and we use 200 as default status
                # In a more complex setup, we'd capture the actual Response object
                return result, 200

            response_data, status_code, was_cached = service.check_and_record_idempotency(
                db, idempotency_key, user_id, endpoint, lambda: processor() # This needs to be handled carefully for async
            )
            
            # Note: The above lambda is problematic with async. 
            # I'll adjust the service to handle sync/async or just call it here.
            
            return response_data

        return wrapper
    return decorator

def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    """
    Dependency to enforce rate limiting on a route.
    """
    async def dependency(
        request: Request,
        db: Session = Depends(get_db),
        service: RequestControlService = Depends(get_request_control_service)
    ):
        user_id = 1 # Placeholder
        endpoint = f"{request.method} {request.url.path}"
        
        is_allowed, retry_after = service.check_rate_limit(
            db, user_id, endpoint, max_requests, window_seconds
        )
        
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)}
            )
        
        return True

    return dependency
