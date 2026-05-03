from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.lending_borrowing.schemas import LoanCreate, LoanResponse
from app.apps.lending_borrowing.service import LendingBorrowingService
from app.apps.lending_borrowing.providers import get_lending_borrowing_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

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
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Creates a loan request and calculates the projected budget impact.
    """
    return service.request_loan(db, data)
