from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.budget_tracker.schemas import BudgetAllocationCreate, BudgetAllocationResponse
from app.apps.budget_tracker.service import BudgetAllocationService
from app.apps.budget_tracker.providers import get_budget_allocation_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.post(
    "/allocate",
    response_model=BudgetAllocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new budget allocation"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def create_allocation(
    request: Request,
    data: BudgetAllocationCreate,
    db: Session = Depends(get_db),
    service: BudgetAllocationService = Depends(get_budget_allocation_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Creates a new budget allocation, ensuring that the total allocations
    do not exceed the total HELB amount.
    """
    return service.allocate_budget(db, data)
