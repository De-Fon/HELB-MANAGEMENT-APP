from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.apps.mpesa_integration.schemas import MpesaSyncRequest, MpesaTransactionResponse
from app.apps.mpesa_integration.service import MpesaTransactionService
from app.apps.mpesa_integration.providers import get_mpesa_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

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
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Syncs a list of M-Pesa transactions, ignoring any duplicates.
    """
    return service.sync_transactions(db, data.user_id, data.transactions)
