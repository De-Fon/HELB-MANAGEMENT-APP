from sqlalchemy.orm import Session
from app.apps.lending_borrowing.models import Loan
from app.apps.lending_borrowing.schemas import LoanCreate

class LendingBorrowingRepository:
    def create_loan_request(self, db: Session, data: LoanCreate) -> Loan:
        """Persists a new loan request."""
        db_loan = Loan(**data.model_dump())
        db.add(db_loan)
        db.flush()
        db.refresh(db_loan)
        return db_loan
