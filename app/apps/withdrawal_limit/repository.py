from sqlalchemy.orm import Session
from typing import Optional
from app.apps.withdrawal_limit.models import WithdrawalLimitSetting
from app.shared.utils import get_current_utc_time

class WithdrawalLimitRepository:
    def get_limit_for_update(self, db: Session, user_id: int) -> Optional[WithdrawalLimitSetting]:
        """Fetch limit setting with row-level locking."""
        return db.query(WithdrawalLimitSetting).filter(
            WithdrawalLimitSetting.user_id == user_id
        ).with_for_update().first()

    def create_default_limit(self, db: Session, user_id: int) -> WithdrawalLimitSetting:
        """Creates a default limit setting for a new user."""
        setting = WithdrawalLimitSetting(
            user_id=user_id,
            daily_limit_amount=1000.0,
            current_daily_withdrawn=0.0,
            last_reset_date=get_current_utc_time().date()
        )
        db.add(setting)
        db.flush()
        return setting

    def update_limit(self, db: Session, setting: WithdrawalLimitSetting, withdrawn_today: float):
        """Update daily withdrawn amount."""
        setting.current_daily_withdrawn = withdrawn_today
        db.flush()
        return setting

    def reset_daily_limit(self, db: Session, setting: WithdrawalLimitSetting):
        """Reset daily withdrawn amount and update reset date."""
        setting.current_daily_withdrawn = 0.0
        setting.last_reset_date = get_current_utc_time().date()
        db.flush()
        return setting
