from fastapi import Depends
from app.apps.scholarship_tracker.repository import ScholarshipRepository
from app.apps.scholarship_tracker.service import ScholarshipService
from app.apps.request_control.providers import get_idempotency_service, get_rate_limit_service

def get_scholarship_repository() -> ScholarshipRepository:
    return ScholarshipRepository()

def get_scholarship_service(
    repo: ScholarshipRepository = Depends(get_scholarship_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> ScholarshipService:
    return ScholarshipService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
