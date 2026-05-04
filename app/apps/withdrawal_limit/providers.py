from fastapi import Depends
from app.apps.withdrawal_limit.repository import WithdrawalLimitRepository
from app.apps.withdrawal_limit.service import WithdrawalLimitService
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service

def get_withdrawal_limit_repository() -> WithdrawalLimitRepository:
    return WithdrawalLimitRepository()

def get_withdrawal_limit_service(
    repo: WithdrawalLimitRepository = Depends(get_withdrawal_limit_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> WithdrawalLimitService:
    return WithdrawalLimitService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
