from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.emergency_fund.schemas import EmergencyFundWithdraw, EmergencyFundResponse
from app.apps.emergency_fund.service import EmergencyFundService
from app.apps.emergency_fund.providers import get_emergency_fund_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.post(
    "/withdraw",
    response_model=EmergencyFundResponse,
    status_code=status.HTTP_200_OK,
    summary="Withdraw from emergency fund"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def withdraw_from_emergency(
    request: Request,
    data: EmergencyFundWithdraw, # Renamed from 'request' to avoid shadowing
    db: Session = Depends(get_db),
    service: EmergencyFundService = Depends(get_emergency_fund_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Withdraws a specified amount from the user's emergency fund, 
    ensuring they have sufficient remaining balance.
    """
    return service.withdraw_from_emergency(db, data.user_id, data.amount)
