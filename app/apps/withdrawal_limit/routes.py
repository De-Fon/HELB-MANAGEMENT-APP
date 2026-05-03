from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.withdrawal_limit.schemas import WithdrawalLimitResponse
from app.apps.withdrawal_limit.service import WithdrawalLimitService
from app.apps.withdrawal_limit.providers import get_withdrawal_limit_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

router = APIRouter()

@router.get(
    "/{user_id}/check",
    response_model=WithdrawalLimitResponse,
    status_code=status.HTTP_200_OK,
    summary="Check withdrawal eligibility"
)
@rate_limit(max_requests=30, window_seconds=60)
def check_limit(
    request: Request,
    user_id: int,
    amount: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    service: WithdrawalLimitService = Depends(get_withdrawal_limit_service),
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Checks if a user is eligible to withdraw the requested amount
    based on their daily limit.
    """
    eligible, remaining, limit_obj = service.check_withdrawal_eligibility(db, user_id, amount)
    
    return WithdrawalLimitResponse(
        user_id=limit_obj.user_id,
        daily_limit_amount=limit_obj.daily_limit_amount,
        current_daily_withdrawn=limit_obj.current_daily_withdrawn,
        remaining_today=remaining,
        eligible=eligible
    )
