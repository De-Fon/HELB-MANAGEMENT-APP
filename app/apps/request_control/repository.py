from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.apps.request_control.models import IdempotencyRecord, RateLimitRecord
from app.shared.utils import get_current_utc_time

class RequestControlRepository:
    def get_idempotency_record(
        self, db: Session, key: str, user_id: int, endpoint: str
    ) -> Optional[IdempotencyRecord]:
        now = get_current_utc_time()
        return db.query(IdempotencyRecord).filter(
            and_(
                IdempotencyRecord.idempotency_key == key,
                IdempotencyRecord.user_id == user_id,
                IdempotencyRecord.endpoint == endpoint,
                IdempotencyRecord.expires_at > now
            )
        ).first()

    def save_idempotency_record(
        self, db: Session, key: str, user_id: int, endpoint: str, 
        status_code: int, response_body: Any, ttl_hours: int = 24
    ) -> IdempotencyRecord:
        now = get_current_utc_time()
        expires_at = now + timedelta(hours=ttl_hours)
        
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

    def increment_rate_limit(
        self, db: Session, user_id: int, endpoint: str, window_seconds: int
    ) -> Dict[str, Any]:
        now = get_current_utc_time()
        
        # Check if there is an active window
        record = db.query(RateLimitRecord).filter(
            and_(
                RateLimitRecord.user_id == user_id,
                RateLimitRecord.endpoint == endpoint,
                RateLimitRecord.window_end > now
            )
        ).first()

        if record:
            record.request_count += 1
            db.flush()
        else:
            # Create new window
            window_start = now
            window_end = now + timedelta(seconds=window_seconds)
            record = RateLimitRecord(
                user_id=user_id,
                endpoint=endpoint,
                request_count=1,
                window_start=window_start,
                window_end=window_end
            )
            db.add(record)
            db.flush()

        return {
            "count": record.request_count,
            "window_start": record.window_start,
            "window_end": record.window_end
        }
