from sqlalchemy.orm import Session
from app.apps.lending_borrowing.repository import LendingBorrowingRepository
from app.apps.lending_borrowing.schemas import LoanCreate

class LendingBorrowingService:
    def __init__(self, repository: LendingBorrowingRepository):
        self.repository = repository

    def calculate_loan_impact(self, lender_id: int, borrower_id: int, amount: float):
        # Calculate the impact: Lender loses amount, borrower gains amount.
        return {
            f"user_{lender_id}_balance_change": -amount,
            f"user_{borrower_id}_balance_change": amount
        }

    def request_loan(self, db: Session, data: LoanCreate):
        db_loan = self.repository.create_loan(db, data)
        db.commit()
        impact = self.calculate_loan_impact(data.lender_user_id, data.borrower_user_id, data.amount)
        return {"loan": db_loan, "impact": impact}
