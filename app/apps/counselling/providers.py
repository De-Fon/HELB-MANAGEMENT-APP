from fastapi import Depends
from app.apps.counselling.repository import CounsellingRepository
from app.apps.counselling.service import CounsellingService
from app.apps.request_control.providers import get_idempotency_service, get_rate_limit_service

def get_counselling_repository() -> CounsellingRepository:
    return CounsellingRepository()

def get_counselling_service(
    repo: CounsellingRepository = Depends(get_counselling_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> CounsellingService:
    return CounsellingService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
