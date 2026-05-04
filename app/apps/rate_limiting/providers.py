from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.rate_limiting.repository import RateLimitRepository
from app.apps.rate_limiting.service import RateLimitService

def get_rate_limit_repository() -> RateLimitRepository:
    return RateLimitRepository()

def get_rate_limit_service(
    repository: RateLimitRepository = Depends(get_rate_limit_repository)
) -> RateLimitService:
    return RateLimitService(repository)
