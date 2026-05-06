from sqlalchemy.orm import Session
from typing import List, Dict
from app.apps.offline_sync.repository import OfflineSyncRepository
from app.apps.offline_sync.models import OfflineQueue

class OfflineSyncService:
    def __init__(
        self, 
        repository: OfflineSyncRepository,
        idempotency_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
    def sync_queued_actions(self, db: Session, user_id: int) -> List[Dict]:
        """
        Processes all unsynced actions. 
        Wrapped in a single transaction for atomicity.
        """
        unsynced = self.repository.get_unsynced_actions(db, user_id)
        results = []
        
        try:
            for action in unsynced:
                # Simulation of dynamic routing logic
                synced_item = self.repository.mark_as_synced(db, action.id)
                results.append(synced_item)
                
            db.commit()
            return results
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Sync failed: {str(e)}"
            )
