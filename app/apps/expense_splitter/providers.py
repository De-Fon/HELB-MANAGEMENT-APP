from fastapi import Depends
from app.apps.expense_splitter.repository import ExpenseSplitterRepository
from app.apps.expense_splitter.service import ExpenseSplitterService
from app.apps.idempotency.providers import get_idempotency_service

def get_expense_splitter_repository() -> ExpenseSplitterRepository:
    return ExpenseSplitterRepository()

def get_expense_splitter_service(
    repo: ExpenseSplitterRepository = Depends(get_expense_splitter_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True)
) -> ExpenseSplitterService:
    return ExpenseSplitterService(
        repository=repo,
        idempotency_service=idempotency_service
    )
