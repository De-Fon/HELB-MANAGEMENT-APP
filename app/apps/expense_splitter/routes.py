from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.expense_splitter.schemas import SharedExpenseCreate, SharedExpenseResponse
from app.apps.expense_splitter.service import ExpenseSplitterService
from app.apps.expense_splitter.providers import get_expense_splitter_service

router = APIRouter()

@router.post(
    "/add",
    response_model=SharedExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a shared expense"
)
def add_shared_expense(
    data: SharedExpenseCreate,
    db: Session = Depends(get_db),
    service: ExpenseSplitterService = Depends(get_expense_splitter_service)
):
    """
    Creates a new shared expense and calculates the balance sheet.
    """
    return service.split_expense(db, data)
