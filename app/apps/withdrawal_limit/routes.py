from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.withdrawal_limit.schemas import WithdrawalLimitResponse
from app.apps.withdrawal_limit.service import WithdrawalLimitService
from app.apps.withdrawal_limit.providers import get_withdrawal_limit_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

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
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
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
