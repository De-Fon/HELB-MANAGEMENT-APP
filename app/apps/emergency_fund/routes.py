from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.emergency_fund.schemas import EmergencyFundWithdraw, EmergencyFundResponse
from app.apps.emergency_fund.service import EmergencyFundService
from app.apps.emergency_fund.providers import get_emergency_fund_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/withdraw",
    response_model=EmergencyFundResponse,
    status_code=status.HTTP_200_OK,
    summary="Withdraw from emergency fund"
)
@idempotent()
@limiter.limit("5/minute")
def withdraw_from_emergency(
    request: Request,
    response: Response,
    data: EmergencyFundWithdraw, # Renamed from 'request' to avoid shadowing
    db: Session = Depends(get_db),
    service: EmergencyFundService = Depends(get_emergency_fund_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Withdraws a specified amount from the user's emergency fund, 
    ensuring they have sufficient remaining balance.
    """
    return service.withdraw_from_emergency(db, data.user_id, data.amount)
