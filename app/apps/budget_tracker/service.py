from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.budget_tracker.repository import BudgetAllocationRepository
from app.apps.budget_tracker.schemas import BudgetAllocationCreate
from app.apps.budget_tracker.models import BudgetAllocation

class BudgetAllocationService:
    def __init__(
        self, 
        repository: BudgetAllocationRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def allocate_budget(self, db: Session, data: BudgetAllocationCreate) -> BudgetAllocation:
        total_allocations = (
            data.rent_allocation +
            data.food_allocation +
            data.transport_allocation +
            data.personal_needs_allocation
        )

        if total_allocations > data.total_helb_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total allocations exceed the total HELB amount."
            )

        allocation = self.repository.create_budget_allocation(db, data)
        db.commit()
        return allocation
