from fastapi import Depends
from app.apps.withdrawal_limit.repository import WithdrawalLimitRepository
from app.apps.withdrawal_limit.service import WithdrawalLimitService

def get_withdrawal_limit_repository() -> WithdrawalLimitRepository:
    return WithdrawalLimitRepository()

def get_withdrawal_limit_service(
    repo: WithdrawalLimitRepository = Depends(get_withdrawal_limit_repository)
) -> WithdrawalLimitService:
    return WithdrawalLimitService(repository=repo)
