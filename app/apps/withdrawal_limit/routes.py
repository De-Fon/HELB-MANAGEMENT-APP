from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.withdrawal_limit.schemas import WithdrawalLimitResponse
from app.apps.withdrawal_limit.service import WithdrawalLimitService
from app.apps.withdrawal_limit.providers import get_withdrawal_limit_service

router = APIRouter()

@router.get(
    "/{user_id}/check",
    response_model=WithdrawalLimitResponse,
    status_code=status.HTTP_200_OK,
    summary="Check withdrawal eligibility"
)
def check_limit(
    user_id: int,
    amount: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    service: WithdrawalLimitService = Depends(get_withdrawal_limit_service)
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
