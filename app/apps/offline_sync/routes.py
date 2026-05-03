from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.offline_sync.schemas import OfflineQueueResponse
from app.apps.offline_sync.service import OfflineSyncService
from app.apps.offline_sync.providers import get_offline_sync_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

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
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Processes all unsynced actions for a user from the offline queue.
    """
    return service.sync_queued_actions(db, user_id)
