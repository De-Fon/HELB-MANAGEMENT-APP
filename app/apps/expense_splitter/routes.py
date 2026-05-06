from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.expense_splitter.schemas import SharedExpenseCreate, SharedExpenseResponse
from app.apps.expense_splitter.service import ExpenseSplitterService
from app.apps.expense_splitter.providers import get_expense_splitter_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/add",
    response_model=SharedExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a shared expense"
)
@idempotent()
@limiter.limit("5/minute")
def add_shared_expense(
    request: Request,
    response: Response,
    data: SharedExpenseCreate,
    db: Session = Depends(get_db),
    service: ExpenseSplitterService = Depends(get_expense_splitter_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Creates a new shared expense and calculates the balance sheet.
    """
    return service.split_expense(db, data)
