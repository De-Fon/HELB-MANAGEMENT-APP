from sqlalchemy.orm import Session
from app.apps.budget_tracker.models import BudgetAllocation
from app.apps.budget_tracker.schemas import BudgetAllocationCreate

class BudgetAllocationRepository:
    def create_budget_allocation(self, db: Session, data: BudgetAllocationCreate) -> BudgetAllocation:
        db_allocation = BudgetAllocation(**data.model_dump())
        db.add(db_allocation)
        db.flush()
        db.refresh(db_allocation)
        return db_allocation
