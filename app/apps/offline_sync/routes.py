from fastapi import APIRouter, Depends, status, Query, Request, Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.offline_sync.schemas import OfflineQueueResponse
from app.apps.offline_sync.service import OfflineSyncService
from app.apps.offline_sync.providers import get_offline_sync_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/sync",
    response_model=List[OfflineQueueResponse],
    status_code=status.HTTP_200_OK,
    summary="Sync offline actions"
)
@idempotent()
@limiter.limit("5/minute")
def sync_offline_actions(
    request: Request,
    response: Response,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
    service: OfflineSyncService = Depends(get_offline_sync_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Processes all unsynced actions for a user from the offline queue.
    """
    return service.sync_queued_actions(db, user_id)
