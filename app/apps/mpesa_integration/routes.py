from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.apps.mpesa_integration.schemas import MpesaSyncRequest, MpesaTransactionResponse
from app.apps.mpesa_integration.service import MpesaTransactionService
from app.apps.mpesa_integration.providers import get_mpesa_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

router = APIRouter()

@router.post(
    "/sync",
    response_model=List[MpesaTransactionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Sync M-Pesa transactions"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def sync_mpesa_transactions(
    request: Request,
    data: MpesaSyncRequest, # Renamed from 'request' to avoid shadowing
    db: Session = Depends(get_db),
    service: MpesaTransactionService = Depends(get_mpesa_service),
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Syncs a list of M-Pesa transactions, ignoring any duplicates.
    """
    return service.sync_transactions(db, data.user_id, data.transactions)
