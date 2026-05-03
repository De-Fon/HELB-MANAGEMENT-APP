from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.expenditure_analytics.schemas import ExpenditureReport
from app.apps.expenditure_analytics.service import ExpenditureAnalyticsService
from app.apps.expenditure_analytics.providers import get_expenditure_service

router = APIRouter()

@router.get(
    "/report/{user_id}",
    response_model=ExpenditureReport,
    status_code=status.HTTP_200_OK,
    summary="Get expenditure comparison report"
)
def get_expenditure_report(
    user_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., gt=2000),
    db: Session = Depends(get_db),
    service: ExpenditureAnalyticsService = Depends(get_expenditure_service)
):
    """
    Generates a comparison report for the user's expenditures vs peer averages.
    """
    return service.generate_comparison_report(db, user_id, month, year)
