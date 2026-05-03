from sqlalchemy.orm import Session
from sqlalchemy import and_, update
from datetime import timedelta
from typing import Optional, Dict, Any
from app.apps.request_control.models import IdempotencyRecord, RateLimitRecord
from app.shared.utils import get_current_utc_time

class RequestControlRepository:
    def get_idempotency(
        self, db: Session, key: str, user_id: int, endpoint: str
    ) -> Optional[IdempotencyRecord]:
        """Fetch active idempotency record."""
        return db.query(IdempotencyRecord).filter(
            and_(
                IdempotencyRecord.idempotency_key == key,
                IdempotencyRecord.user_id == user_id,
                IdempotencyRecord.endpoint == endpoint,
                IdempotencyRecord.expires_at > get_current_utc_time()
            )
        ).first()

    def create_idempotency(
        self, db: Session, key: str, user_id: int, endpoint: str, 
        status_code: int, response_body: Any, ttl_hours: int = 24
    ) -> IdempotencyRecord:
        """Create a new idempotency record with TTL."""
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

    def get_active_rate_limit(
        self, db: Session, user_id: int, endpoint: str
    ) -> Optional[RateLimitRecord]:
        """Fetch current active rate limit window."""
        return db.query(RateLimitRecord).filter(
            and_(
                RateLimitRecord.user_id == user_id,
                RateLimitRecord.endpoint == endpoint,
                RateLimitRecord.window_end > get_current_utc_time()
            )
        ).first()

    def increment_rate_limit(self, db: Session, record_id: int):
        """Atomsically increment the request count for a specific record."""
        db.execute(
            update(RateLimitRecord)
            .where(RateLimitRecord.id == record_id)
            .values(request_count=RateLimitRecord.request_count + 1)
        )
        db.flush()

    def create_rate_limit_window(
        self, db: Session, user_id: int, endpoint: str, window_seconds: int
    ) -> RateLimitRecord:
        """Initialize a new rate limit window."""
        now = get_current_utc_time()
        record = RateLimitRecord(
            user_id=user_id,
            endpoint=endpoint,
            request_count=1,
            window_start=now,
            window_end=now + timedelta(seconds=window_seconds)
        )
        db.add(record)
        db.flush()
        return record
