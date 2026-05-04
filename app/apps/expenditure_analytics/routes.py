from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.expenditure_analytics.schemas import ExpenditureReport
from app.apps.expenditure_analytics.service import ExpenditureAnalyticsService
from app.apps.expenditure_analytics.providers import get_expenditure_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.get(
    "/report/{user_id}",
    response_model=ExpenditureReport,
    status_code=status.HTTP_200_OK,
    summary="Get expenditure comparison report"
)
@rate_limit(max_requests=30, window_seconds=60)
def get_expenditure_report(
    request: Request,
    user_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., gt=2000),
    db: Session = Depends(get_db),
    service: ExpenditureAnalyticsService = Depends(get_expenditure_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Generates a comparison report for the user's expenditures vs peer averages.
    """
    return service.generate_comparison_report(db, user_id, month, year)
