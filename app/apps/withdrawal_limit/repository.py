from sqlalchemy.orm import Session
from sqlalchemy import func
from app.apps.withdrawal_limit.models import WithdrawalLimitSetting

class WithdrawalLimitRepository:
    def get_or_create_limit(self, db: Session, user_id: int) -> WithdrawalLimitSetting:
        setting = db.query(WithdrawalLimitSetting).filter(WithdrawalLimitSetting.user_id == user_id).with_for_update().first()
        if not setting:
            setting = WithdrawalLimitSetting(
                user_id=user_id,
                daily_limit_amount=1000.0, # Default value
                current_daily_withdrawn=0.0
            )
            db.add(setting)
            db.flush()
            db.refresh(setting)
        return setting
