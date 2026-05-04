from sqlalchemy.orm import Session
from sqlalchemy import update
from datetime import timedelta
from typing import Optional
from app.apps.rate_limiting.models import RateLimitRecord
from app.shared.utils import get_current_utc_time

class RateLimitRepository:
    def get_active_rate_limit(self, db: Session, user_id: int, endpoint: str) -> Optional[RateLimitRecord]:
        """Fetch the current rate limit window if it hasn't expired."""
        now = get_current_utc_time()
        return db.query(RateLimitRecord).filter(
            RateLimitRecord.user_id == user_id,
            RateLimitRecord.endpoint == endpoint,
            RateLimitRecord.window_end > now
        ).first()

    def increment_rate_limit(self, db: Session, record_id: int):
        """Atomic increment to prevent race conditions."""
        stmt = update(RateLimitRecord).where(
            RateLimitRecord.id == record_id
        ).values(
            request_count=RateLimitRecord.request_count + 1
        )
        db.execute(stmt)

    def create_rate_limit_window(self, db: Session, user_id: int, endpoint: str, window_seconds: int) -> RateLimitRecord:
        """Starts a new rate limiting window."""
        now = get_current_utc_time()
        window_end = now + timedelta(seconds=window_seconds)
        
        record = RateLimitRecord(
            user_id=user_id,
            endpoint=endpoint,
            window_start=now,
            window_end=window_end,
            request_count=1
        )
        db.add(record)
        db.flush()
        return record
