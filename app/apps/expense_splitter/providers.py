from fastapi import Depends
from app.apps.expense_splitter.repository import ExpenseSplitterRepository
from app.apps.expense_splitter.service import ExpenseSplitterService

def get_expense_splitter_repository() -> ExpenseSplitterRepository:
    return ExpenseSplitterRepository()

def get_expense_splitter_service(
    repo: ExpenseSplitterRepository = Depends(get_expense_splitter_repository)
) -> ExpenseSplitterService:
    return ExpenseSplitterService(repository=repo)
