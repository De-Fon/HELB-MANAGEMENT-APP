from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.idempotency.repository import IdempotencyRepository
from app.apps.idempotency.service import IdempotencyService

def get_idempotency_repository() -> IdempotencyRepository:
    return IdempotencyRepository()

def get_idempotency_service(
    repository: IdempotencyRepository = Depends(get_idempotency_repository)
) -> IdempotencyService:
    return IdempotencyService(repository)

