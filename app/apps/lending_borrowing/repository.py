from sqlalchemy.orm import Session
from app.apps.lending_borrowing.models import Loan
from app.apps.lending_borrowing.schemas import LoanCreate

class LendingBorrowingRepository:
    def create_loan(self, db: Session, data: LoanCreate) -> Loan:
        db_loan = Loan(**data.model_dump())
        db.add(db_loan)
        db.flush()
        db.refresh(db_loan)
        return db_loan
