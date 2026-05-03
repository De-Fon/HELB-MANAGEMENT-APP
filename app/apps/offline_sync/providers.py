from fastapi import Depends
from app.apps.offline_sync.repository import OfflineSyncRepository
from app.apps.offline_sync.service import OfflineSyncService

def get_offline_sync_repository() -> OfflineSyncRepository:
    return OfflineSyncRepository()

def get_offline_sync_service(
    repo: OfflineSyncRepository = Depends(get_offline_sync_repository)
) -> OfflineSyncService:
    return OfflineSyncService(repository=repo)
