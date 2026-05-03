from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.lending_borrowing.schemas import LoanCreate, LoanRequestResponse
from app.apps.lending_borrowing.service import LendingBorrowingService
from app.apps.lending_borrowing.providers import get_lending_borrowing_service

router = APIRouter()

@router.post(
    "/request",
    response_model=LoanRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Request a new loan"
)
def request_loan(
    data: LoanCreate,
    db: Session = Depends(get_db),
    service: LendingBorrowingService = Depends(get_lending_borrowing_service)
):
    """
    Creates a loan request and calculates the projected budget impact.
    """
    return service.request_loan(db, data)
