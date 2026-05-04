from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.offline_sync.schemas import OfflineQueueResponse
from app.apps.offline_sync.service import OfflineSyncService
from app.apps.offline_sync.providers import get_offline_sync_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.post(
    "/sync",
    response_model=List[OfflineQueueResponse],
    status_code=status.HTTP_200_OK,
    summary="Sync offline actions"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def sync_offline_actions(
    request: Request,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
    service: OfflineSyncService = Depends(get_offline_sync_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Processes all unsynced actions for a user from the offline queue.
    """
    return service.sync_queued_actions(db, user_id)
