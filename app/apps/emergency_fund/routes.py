from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apps.emergency_fund.schemas import EmergencyFundWithdraw, EmergencyFundResponse
from app.apps.emergency_fund.service import EmergencyFundService
from app.apps.emergency_fund.providers import get_emergency_fund_service

router = APIRouter()

@router.post(
    "/withdraw",
    response_model=EmergencyFundResponse,
    status_code=status.HTTP_200_OK,
    summary="Withdraw from emergency fund"
)
def withdraw_from_emergency(
    request: EmergencyFundWithdraw,
    db: Session = Depends(get_db),
    service: EmergencyFundService = Depends(get_emergency_fund_service)
):
    """
    Withdraws a specified amount from the user's emergency fund, 
    ensuring they have sufficient remaining balance.
    """
    return service.withdraw_from_emergency(db, request.user_id, request.amount)
