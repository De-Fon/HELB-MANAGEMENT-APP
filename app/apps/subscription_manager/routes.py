from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.subscription_manager.schemas import SubscriptionResponse
from app.apps.subscription_manager.service import SubscriptionService
from app.apps.subscription_manager.providers import get_subscription_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.get(
    "/upcoming/{user_id}",
    response_model=List[SubscriptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get upcoming subscription renewals"
)
@limiter.limit("30/minute")
def get_upcoming_subscriptions(
    request: Request,
    response: Response,
    user_id: int,
    db: Session = Depends(get_db),
    service: SubscriptionService = Depends(get_subscription_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Checks and alerts users about subscriptions renewing within the next 7 days.
    """
    return service.check_and_alert_renewals(db, user_id)
