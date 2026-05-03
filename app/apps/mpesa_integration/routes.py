from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.apps.mpesa_integration.schemas import MpesaSyncRequest, MpesaTransactionResponse
from app.apps.mpesa_integration.service import MpesaTransactionService
from app.apps.mpesa_integration.providers import get_mpesa_service

router = APIRouter()

@router.post(
    "/sync",
    response_model=List[MpesaTransactionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Sync M-Pesa transactions"
)
def sync_mpesa_transactions(
    request: MpesaSyncRequest,
    db: Session = Depends(get_db),
    service: MpesaTransactionService = Depends(get_mpesa_service)
):
    """
    Syncs a list of M-Pesa transactions, ignoring any duplicates.
    """
    return service.sync_transactions(db, request.user_id, request.transactions)
