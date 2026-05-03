from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Any, Tuple, Optional
from app.apps.request_control.repository import RequestControlRepository
from app.shared.utils import get_current_utc_time

class RequestControlService:
    def __init__(self, repository: RequestControlRepository):
        self.repository = repository

    def get_cached_response(
        self, db: Session, key: str, user_id: int, endpoint: str
    ) -> Optional[Tuple[Any, int]]:
        """Checks if a valid cached response exists for the given key and endpoint."""
        record = self.repository.get_idempotency(db, key, user_id, endpoint)
        if record:
            return record.response_body, record.status_code
        return None

    def store_idempotent_response(
        self, db: Session, key: str, user_id: int, endpoint: str, 
        status_code: int, response_body: Any
    ):
        """Stores the response of a successful request for future idempotency checks."""
        self.repository.create_idempotency(
            db, key, user_id, endpoint, status_code, response_body
        )
        db.commit()

    def validate_rate_limit(
        self, db: Session, user_id: int, endpoint: str, 
        max_requests: int, window_seconds: int
    ) -> Optional[int]:
        """
        Validates rate limits using atomic increments. 
        Returns None if allowed, or retry_after seconds if blocked.
        """
        record = self.repository.get_active_rate_limit(db, user_id, endpoint)
        
        if record:
            self.repository.increment_rate_limit(db, record.id)
            db.refresh(record) # Get the updated count
        else:
            record = self.repository.create_rate_limit_window(db, user_id, endpoint, window_seconds)
        
        db.commit()

        if record.request_count > max_requests:
            now = get_current_utc_time()
            retry_after = int((record.window_end - now).total_seconds())
            return max(0, retry_after)
        
        return None

    def resolve_endpoint_id(self, method: str, path: str) -> str:
        """Utility to generate a consistent endpoint identifier."""
        return f"{method.upper()} {path}"
