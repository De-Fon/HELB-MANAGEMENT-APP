from fastapi import Depends
from app.apps.mpesa_integration.repository import MpesaTransactionRepository
from app.apps.mpesa_integration.service import MpesaTransactionService
from app.apps.request_control.providers import get_idempotency_service, get_rate_limit_service

def get_mpesa_repository() -> MpesaTransactionRepository:
    return MpesaTransactionRepository()

def get_mpesa_service(
    repo: MpesaTransactionRepository = Depends(get_mpesa_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> MpesaTransactionService:
    return MpesaTransactionService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
