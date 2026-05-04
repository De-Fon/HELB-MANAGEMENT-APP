from sqlalchemy.orm import Session
from typing import Optional, Tuple, Any
from app.apps.idempotency.repository import IdempotencyRepository

class IdempotencyService:
    def __init__(self, repository: IdempotencyRepository):
        self.repository = repository

    def get_cached_response(self, db: Session, key: str, user_id: int, endpoint: str) -> Optional[Tuple[Any, int]]:
        """Returns (body, status_code) if found, else None."""
        record = self.repository.get_idempotency(db, key, user_id, endpoint)
        if record:
            return record.response_body, record.status_code
        return None

    def save_response(self, db: Session, key: str, user_id: int, endpoint: str, status_code: int, response_body: Any):
        """Caches a successful response."""
        # Only cache successful/created responses (200, 201)
        if 200 <= status_code < 300:
            self.repository.create_idempotency(db, key, user_id, endpoint, status_code, response_body)
            db.commit()
