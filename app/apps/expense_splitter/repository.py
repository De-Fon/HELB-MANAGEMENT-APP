from sqlalchemy.orm import Session
from app.apps.expense_splitter.models import SharedExpense
from app.apps.expense_splitter.schemas import SharedExpenseCreate

class ExpenseSplitterRepository:
    def create_expense(self, db: Session, data: SharedExpenseCreate) -> SharedExpense:
        db_expense = SharedExpense(**data.model_dump())
        db.add(db_expense)
        db.flush()
        db.refresh(db_expense)
        return db_expense
