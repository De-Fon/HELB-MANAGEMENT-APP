from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from app.apps.offline_sync.models import OfflineQueue
from app.apps.offline_sync.schemas import OfflineActionCreate

class OfflineSyncRepository:
    def save_offline_action(self, db: Session, data: OfflineActionCreate) -> OfflineQueue:
        db_queue = OfflineQueue(**data.model_dump())
        db.add(db_queue)
        db.flush()
        db.refresh(db_queue)
        return db_queue

    def get_unsynced_actions(self, db: Session, user_id: int) -> List[OfflineQueue]:
        return db.query(OfflineQueue).filter(
            OfflineQueue.user_id == user_id,
            OfflineQueue.synced_at == None
        ).order_by(OfflineQueue.created_at.asc()).with_for_update(skip_locked=True).all()

    def mark_as_synced(self, db: Session, queue_id: int) -> OfflineQueue:
        queue_item = db.query(OfflineQueue).filter(OfflineQueue.id == queue_id).first()
        if queue_item:
            queue_item.synced_at = datetime.now(timezone.utc)
            db.flush()
            db.refresh(queue_item)
        return queue_item
