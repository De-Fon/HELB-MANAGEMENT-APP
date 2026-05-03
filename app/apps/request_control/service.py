from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Callable, Any, Tuple
from app.apps.request_control.repository import RequestControlRepository
from app.shared.utils import get_current_utc_time

class RequestControlService:
    def __init__(self, repository: RequestControlRepository):
        self.repository = repository

    def check_and_record_idempotency(
        self, db: Session, key: str, user_id: int, endpoint: str, 
        request_processor: Callable[[], Any]
    ) -> Tuple[Any, int, bool]:
        """
        Checks if a request with the given key exists.
        If yes, returns the cached response.
        If no, processes the request, saves the result, and returns it.
        """
        existing_record = self.repository.get_idempotency_record(db, key, user_id, endpoint)
        
        if existing_record:
            return existing_record.response_body, existing_record.status_code, True
        
        # Process new request
        try:
            response_data, status_code = request_processor()
            
            # Save the record
            self.repository.save_idempotency_record(
                db, key, user_id, endpoint, status_code, response_data
            )
            db.commit()
            
            return response_data, status_code, False
        except Exception as e:
            db.rollback()
            raise e

    def check_rate_limit(
        self, db: Session, user_id: int, endpoint: str, 
        max_requests: int, window_seconds: int
    ) -> Tuple[bool, int]:
        """
        Validates rate limits for a user and endpoint.
        Returns (is_allowed, retry_after_seconds).
        """
        result = self.repository.increment_rate_limit(db, user_id, endpoint, window_seconds)
        db.commit()
        
        count = result["count"]
        window_end = result["window_end"]
        
        if count > max_requests:
            now = get_current_utc_time()
            retry_after = int((window_end - now).total_seconds())
            return False, max(0, retry_after)
        
        return True, 0
