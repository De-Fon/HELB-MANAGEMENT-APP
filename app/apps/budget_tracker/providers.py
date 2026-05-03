from fastapi import Depends
from app.apps.budget_tracker.repository import BudgetAllocationRepository
from app.apps.budget_tracker.service import BudgetAllocationService

def get_budget_allocation_repository() -> BudgetAllocationRepository:
    return BudgetAllocationRepository()

def get_budget_allocation_service(
    repo: BudgetAllocationRepository = Depends(get_budget_allocation_repository)
) -> BudgetAllocationService:
    return BudgetAllocationService(repository=repo)
