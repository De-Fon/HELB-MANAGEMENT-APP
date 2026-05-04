from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.lending_borrowing.schemas import LoanCreate, LoanResponse
from app.apps.lending_borrowing.service import LendingBorrowingService
from app.apps.lending_borrowing.providers import get_lending_borrowing_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.post(
    "/request",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Request a new loan"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def request_loan(
    request: Request,
    data: LoanCreate,
    db: Session = Depends(get_db),
    service: LendingBorrowingService = Depends(get_lending_borrowing_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Creates a loan request and calculates the projected budget impact.
    """
    return service.request_loan(db, data)
