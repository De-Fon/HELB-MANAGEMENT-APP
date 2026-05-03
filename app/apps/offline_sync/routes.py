from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.offline_sync.schemas import OfflineQueueResponse
from app.apps.offline_sync.service import OfflineSyncService
from app.apps.offline_sync.providers import get_offline_sync_service

router = APIRouter()

@router.post(
    "/sync",
    response_model=List[OfflineQueueResponse],
    status_code=status.HTTP_200_OK,
    summary="Sync offline actions"
)
def sync_offline_actions(
    user_id: int = Query(...),
    db: Session = Depends(get_db),
    service: OfflineSyncService = Depends(get_offline_sync_service)
):
    """
    Processes all unsynced actions for a user from the offline queue.
    """
    return service.sync_queued_actions(db, user_id)
