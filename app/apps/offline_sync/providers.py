from fastapi import Depends
from app.apps.offline_sync.repository import OfflineSyncRepository
from app.apps.offline_sync.service import OfflineSyncService
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service

def get_offline_sync_repository() -> OfflineSyncRepository:
    return OfflineSyncRepository()

def get_offline_sync_service(
    repo: OfflineSyncRepository = Depends(get_offline_sync_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> OfflineSyncService:
    return OfflineSyncService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
