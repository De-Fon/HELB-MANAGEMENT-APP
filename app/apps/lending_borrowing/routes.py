from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.lending_borrowing.schemas import LoanCreate, LoanResponse
from app.apps.lending_borrowing.service import LendingBorrowingService
from app.apps.lending_borrowing.providers import get_lending_borrowing_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/request",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Request a new loan"
)
@idempotent()
@limiter.limit("5/minute")
def request_loan(
    request: Request,
    response: Response,
    data: LoanCreate,
    db: Session = Depends(get_db),
    service: LendingBorrowingService = Depends(get_lending_borrowing_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Creates a loan request and calculates the projected budget impact.
    """
    return service.request_loan(db, data)
