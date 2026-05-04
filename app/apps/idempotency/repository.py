from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional, Any
from app.apps.idempotency.models import IdempotencyRecord
from app.shared.utils import get_current_utc_time

class IdempotencyRepository:
    def get_idempotency(self, db: Session, key: str, user_id: int, endpoint: str) -> Optional[IdempotencyRecord]:
        """Checks for an existing, non-expired idempotency record."""
        now = get_current_utc_time()
        return db.query(IdempotencyRecord).filter(
            IdempotencyRecord.idempotency_key == key,
            IdempotencyRecord.user_id == user_id,
            IdempotencyRecord.endpoint == endpoint,
            IdempotencyRecord.expires_at > now
        ).first()

    def create_idempotency(
        self, db: Session, key: str, user_id: int, endpoint: str, 
        status_code: int, response_body: Any, ttl_hours: int = 24
    ) -> IdempotencyRecord:
        """Stores a successful response for future replay."""
        expires_at = get_current_utc_time() + timedelta(hours=ttl_hours)
        
        record = IdempotencyRecord(
            idempotency_key=key,
            user_id=user_id,
            endpoint=endpoint,
            status_code=status_code,
            response_body=response_body,
            expires_at=expires_at
        )
        db.add(record)
        db.flush()
        return record
