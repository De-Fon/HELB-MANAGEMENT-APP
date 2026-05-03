from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.emergency_fund.schemas import EmergencyFundWithdraw, EmergencyFundResponse
from app.apps.emergency_fund.service import EmergencyFundService
from app.apps.emergency_fund.providers import get_emergency_fund_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

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
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Withdraws a specified amount from the user's emergency fund, 
    ensuring they have sufficient remaining balance.
    """
    return service.withdraw_from_emergency(db, data.user_id, data.amount)
