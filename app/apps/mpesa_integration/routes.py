from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.mpesa_integration.schemas import MpesaSyncRequest, MpesaTransactionResponse
from app.apps.mpesa_integration.service import MpesaTransactionService
from app.apps.mpesa_integration.providers import get_mpesa_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/sync",
    response_model=List[MpesaTransactionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Sync M-Pesa transactions"
)
@idempotent()
@limiter.limit("5/minute")
def sync_mpesa_transactions(
    request: Request,
    response: Response,
    data: MpesaSyncRequest, # Renamed from 'request' to avoid shadowing
    db: Session = Depends(get_db),
    service: MpesaTransactionService = Depends(get_mpesa_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Syncs a list of M-Pesa transactions, ignoring any duplicates.
    """
    return service.sync_transactions(db, data.user_id, data.transactions)
