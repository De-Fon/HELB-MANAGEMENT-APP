from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.expense_splitter.repository import ExpenseSplitterRepository
from app.apps.expense_splitter.schemas import SharedExpenseCreate

class ExpenseSplitterService:
    def __init__(self, repository: ExpenseSplitterRepository):
        self.repository = repository

    def split_expense(self, db: Session, data: SharedExpenseCreate):
        if not data.split_among_user_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Must split among at least one user.")
            
        # Calculate equal split
        total_users = len(data.split_among_user_ids)
        split_amount = round(data.amount / total_users, 2)
        
        # Balance sheet: how much each user owes the payer
        balance_sheet = {}
        for user_id in data.split_among_user_ids:
            if user_id == data.paid_by_user_id:
                balance_sheet[user_id] = 0.0
            else:
                balance_sheet[user_id] = split_amount
                
        # Call repo
        db_expense = self.repository.create_expense(db, data)
        db.commit()
        
        return {
            "id": db_expense.id,
            "group_id": db_expense.group_id,
            "paid_by_user_id": db_expense.paid_by_user_id,
            "amount": db_expense.amount,
            "description": db_expense.description,
            "split_among_user_ids": db_expense.split_among_user_ids,
            "created_at": db_expense.created_at,
            "calculated_balance_per_user": balance_sheet
        }
