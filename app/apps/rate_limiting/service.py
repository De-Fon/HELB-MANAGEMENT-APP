from sqlalchemy.orm import Session
from app.apps.rate_limiting.repository import RateLimitRepository
from app.shared.utils import get_current_utc_time
from typing import Tuple

class RateLimitService:
    def __init__(self, repository: RateLimitRepository):
        self.repository = repository

    def check_rate_limit(self, db: Session, user_id: int, endpoint: str, max_requests: int, window_seconds: int) -> Tuple[bool, int]:
        """
        Returns (is_allowed, retry_after_seconds).
        """
        record = self.repository.get_active_rate_limit(db, user_id, endpoint)
        
        if not record:
            self.repository.create_rate_limit_window(db, user_id, endpoint, window_seconds)
            db.commit()
            return True, 0
            
        if record.request_count >= max_requests:
            now = get_current_utc_time()
            retry_after = int((record.window_end - now).total_seconds())
            return False, max(0, retry_after)
            
        # Increment count
        self.repository.increment_rate_limit(db, record.id)
        db.commit()
        return True, 0
