from sqlalchemy.orm import Session
from typing import List, Dict
from app.apps.offline_sync.repository import OfflineSyncRepository

class OfflineSyncService:
    def __init__(
        self, 
        repository: OfflineSyncRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def sync_queued_actions(self, db: Session, user_id: int) -> List[Dict]:
        unsynced = self.repository.get_unsynced_actions(db, user_id)
        
        results = []
        for action in unsynced:
            # Here you would dynamically route the action.endpoint and pass payload to the respective service.
            # For now, we simulate a successful sync:
            synced_item = self.repository.mark_as_synced(db, action.id)
            
            results.append({
                "id": synced_item.id,
                "user_id": synced_item.user_id,
                "endpoint": synced_item.endpoint,
                "payload": synced_item.payload,
                "created_at": synced_item.created_at,
                "synced_at": synced_item.synced_at,
                "sync_status": "synced" if synced_item.synced_at else "pending"
            })
            
        db.commit()
        return results
