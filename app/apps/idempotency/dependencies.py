from functools import wraps
from typing import Callable, Any
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from loguru import logger
import asyncio

from app.core.database import get_db
from app.apps.idempotency.service import IdempotencyService
from app.apps.idempotency.providers import get_idempotency_service

def idempotent(header_key: str = "Idempotency-Key"):
    """Decorator to enforce idempotency."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            db: Session = kwargs.get("db")
            service: IdempotencyService = kwargs.get("idempotency_service")

            # Resolve missing dependencies from args if necessary
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not all([request, db, service]):
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            idempotency_key = request.headers.get(header_key)
            if not idempotency_key:
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            # Placeholder for user_id (In production, get from authenticated user)
            user_id = 1 
            endpoint = f"{request.method} {request.url.path}"

            cached = service.get_cached_response(db, idempotency_key, user_id, endpoint)
            if cached:
                logger.info(f"Idempotency hit: {endpoint} [Key: {idempotency_key}]")
                return JSONResponse(content=cached[0], status_code=cached[1])

            # Execute the original function
            response = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            # If it's a DB model, refresh it to ensure all fields are loaded before caching
            if hasattr(response, "__table__"):
                db.refresh(response)

            # Cache the response
            service.save_response(
                db, idempotency_key, user_id, endpoint, 
                status_code=status.HTTP_201_CREATED, 
                response_body=jsonable_encoder(response)
            )

            return response
        return wrapper
    return decorator
