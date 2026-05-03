from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.budget_tracker.schemas import BudgetAllocationCreate, BudgetAllocationResponse
from app.apps.budget_tracker.service import BudgetAllocationService
from app.apps.budget_tracker.providers import get_budget_allocation_service

router = APIRouter()

@router.post(
    "/allocate",
    response_model=BudgetAllocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new budget allocation"
)
def create_allocation(
    data: BudgetAllocationCreate,
    db: Session = Depends(get_db),
    service: BudgetAllocationService = Depends(get_budget_allocation_service)
):
    """
    Creates a new budget allocation, ensuring that the total allocations
    do not exceed the total HELB amount.
    """
    return service.allocate_budget(db, data)
