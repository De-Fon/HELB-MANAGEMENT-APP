from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.expense_splitter.schemas import SharedExpenseCreate, SharedExpenseResponse
from app.apps.expense_splitter.service import ExpenseSplitterService
from app.apps.expense_splitter.providers import get_expense_splitter_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

router = APIRouter()

@router.post(
    "/add",
    response_model=SharedExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a shared expense"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def add_shared_expense(
    request: Request,
    data: SharedExpenseCreate,
    db: Session = Depends(get_db),
    service: ExpenseSplitterService = Depends(get_expense_splitter_service),
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Creates a new shared expense and calculates the balance sheet.
    """
    return service.split_expense(db, data)
