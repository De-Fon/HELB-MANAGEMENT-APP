from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.subscription_manager.schemas import SubscriptionResponse
from app.apps.subscription_manager.service import SubscriptionService
from app.apps.subscription_manager.providers import get_subscription_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

router = APIRouter()

@router.get(
    "/upcoming/{user_id}",
    response_model=List[SubscriptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get upcoming subscription renewals"
)
@rate_limit(max_requests=30, window_seconds=60)
def get_upcoming_subscriptions(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    service: SubscriptionService = Depends(get_subscription_service),
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Checks and alerts users about subscriptions renewing within the next 7 days.
    """
    return service.check_and_alert_renewals(db, user_id)
