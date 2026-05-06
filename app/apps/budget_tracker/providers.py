from fastapi import Depends
from app.apps.budget_tracker.repository import BudgetAllocationRepository
from app.apps.budget_tracker.service import BudgetAllocationService
from app.apps.idempotency.providers import get_idempotency_service

def get_budget_allocation_repository() -> BudgetAllocationRepository:
    return BudgetAllocationRepository()

def get_budget_allocation_service(
    repo: BudgetAllocationRepository = Depends(get_budget_allocation_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True)
) -> BudgetAllocationService:
    return BudgetAllocationService(
        repository=repo,
        idempotency_service=idempotency_service
    )
