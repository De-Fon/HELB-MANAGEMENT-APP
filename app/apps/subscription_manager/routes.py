from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.subscription_manager.schemas import SubscriptionResponse
from app.apps.subscription_manager.service import SubscriptionService
from app.apps.subscription_manager.providers import get_subscription_service

router = APIRouter()

@router.get(
    "/upcoming/{user_id}",
    response_model=List[SubscriptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get upcoming subscription renewals"
)
def get_upcoming_subscriptions(
    user_id: int,
    db: Session = Depends(get_db),
    service: SubscriptionService = Depends(get_subscription_service)
):
    """
    Checks and alerts users about subscriptions renewing within the next 7 days.
    """
    return service.check_and_alert_renewals(db, user_id)
