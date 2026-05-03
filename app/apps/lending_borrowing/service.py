from sqlalchemy.orm import Session
from app.apps.lending_borrowing.repository import LendingBorrowingRepository
from app.apps.lending_borrowing.schemas import LoanCreate
from app.apps.lending_borrowing.models import Loan

class LendingBorrowingService:
    def __init__(
        self, 
        repository: LendingBorrowingRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def request_loan(self, db: Session, data: LoanCreate) -> Loan:
        # Business logic for loan requests
        loan = self.repository.create_loan_request(db, data)
        db.commit()
        return loan
