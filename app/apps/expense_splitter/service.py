from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.expense_splitter.repository import ExpenseSplitterRepository
from app.apps.expense_splitter.models import SharedExpense
from app.apps.expense_splitter.schemas import SharedExpenseCreate

class ExpenseSplitterService:
    def __init__(
        self, 
        repository: ExpenseSplitterRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def split_expense(self, db: Session, data: SharedExpenseCreate):
        if not data.split_among_user_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Must split among at least one user.")
            
        # Call repo to persist
        db_expense = self.repository.create_expense(db, data)
        db.commit()
        
        # We attach the calculated balance sheet as a dynamic attribute 
        # so it's included in the response_model serialization
        total_users = len(data.split_among_user_ids)
        split_amount = round(data.amount / total_users, 2)
        
        balance_sheet = {}
        for user_id in data.split_among_user_ids:
            balance_sheet[user_id] = 0.0 if user_id == data.paid_by_user_id else split_amount
            
        db_expense.calculated_balance_per_user = balance_sheet
        return db_expense
