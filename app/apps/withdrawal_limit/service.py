from sqlalchemy.orm import Session
from app.apps.withdrawal_limit.repository import WithdrawalLimitRepository
from app.apps.withdrawal_limit.models import WithdrawalLimitSetting
from app.shared.utils import get_current_utc_time
from typing import Tuple

class WithdrawalLimitService:
    def __init__(
        self, 
        repository: WithdrawalLimitRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def check_withdrawal_eligibility(
        self, db: Session, user_id: int, requested_amount: float
    ) -> Tuple[bool, float, WithdrawalLimitSetting]:
        """
        Validates withdrawal eligibility. 
        Handles daily rollover and concurrency using row-level locking.
        """
        limit = self.repository.get_limit_for_update(db, user_id)
        
        if not limit:
            limit = self.repository.create_default_limit(db, user_id)
        
        # Trigger daily reset if needed
        today = get_current_utc_time().date()
        if limit.last_reset_date != today:
            self.repository.reset_daily_limit(db, limit)

        remaining = limit.daily_limit_amount - limit.current_daily_withdrawn
        eligible = requested_amount <= remaining
        
        db.commit()
        return eligible, remaining, limit
