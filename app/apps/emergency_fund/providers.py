from fastapi import Depends
from app.apps.emergency_fund.repository import EmergencyFundRepository
from app.apps.emergency_fund.service import EmergencyFundService
from app.apps.idempotency.providers import get_idempotency_service

def get_emergency_fund_repository() -> EmergencyFundRepository:
    return EmergencyFundRepository()

def get_emergency_fund_service(
    repo: EmergencyFundRepository = Depends(get_emergency_fund_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True)
) -> EmergencyFundService:
    return EmergencyFundService(
        repository=repo,
        idempotency_service=idempotency_service
    )
