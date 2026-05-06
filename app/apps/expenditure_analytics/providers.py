from fastapi import Depends
from app.apps.expenditure_analytics.repository import ExpenditureAnalyticsRepository
from app.apps.expenditure_analytics.service import ExpenditureAnalyticsService
from app.apps.idempotency.providers import get_idempotency_service

def get_expenditure_repository() -> ExpenditureAnalyticsRepository:
    return ExpenditureAnalyticsRepository()

def get_expenditure_service(
    repo: ExpenditureAnalyticsRepository = Depends(get_expenditure_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True)
) -> ExpenditureAnalyticsService:
    return ExpenditureAnalyticsService(
        repository=repo,
        idempotency_service=idempotency_service
    )
