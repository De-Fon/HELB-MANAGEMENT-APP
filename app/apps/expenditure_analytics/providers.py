from fastapi import Depends
from app.apps.expenditure_analytics.repository import ExpenditureAnalyticsRepository
from app.apps.expenditure_analytics.service import ExpenditureAnalyticsService

def get_expenditure_repository() -> ExpenditureAnalyticsRepository:
    return ExpenditureAnalyticsRepository()

def get_expenditure_service(
    repo: ExpenditureAnalyticsRepository = Depends(get_expenditure_repository)
) -> ExpenditureAnalyticsService:
    return ExpenditureAnalyticsService(repository=repo)
