from fastapi import Depends
from app.apps.lending_borrowing.repository import LendingBorrowingRepository
from app.apps.lending_borrowing.service import LendingBorrowingService
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service

def get_lending_borrowing_repository() -> LendingBorrowingRepository:
    return LendingBorrowingRepository()

def get_lending_borrowing_service(
    repo: LendingBorrowingRepository = Depends(get_lending_borrowing_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> LendingBorrowingService:
    return LendingBorrowingService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
