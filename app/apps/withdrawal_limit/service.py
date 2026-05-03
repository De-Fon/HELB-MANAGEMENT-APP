from sqlalchemy.orm import Session
from datetime import datetime
from app.apps.withdrawal_limit.repository import WithdrawalLimitRepository
from app.apps.withdrawal_limit.models import WithdrawalLimitSetting
from typing import Tuple

class WithdrawalLimitService:
    def __init__(self, repository: WithdrawalLimitRepository):
        self.repository = repository

    def check_withdrawal_eligibility(
        self, db: Session, user_id: int, requested_amount: float
    ) -> Tuple[bool, float, WithdrawalLimitSetting]:
        limit = self.repository.get_or_create_limit(db, user_id)
        
        # Reset logic if date has rolled over
        today = datetime.now().date()
        if limit.last_reset_date != today:
            limit.current_daily_withdrawn = 0.0
            limit.last_reset_date = today

        remaining = limit.daily_limit_amount - limit.current_daily_withdrawn
        eligible = requested_amount <= remaining
        
        db.commit()
        
        return eligible, remaining, limit
