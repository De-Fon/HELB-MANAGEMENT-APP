from sqlalchemy import Column, Integer, Float, DateTime, Date, func
from app.core.database import Base

class WithdrawalLimitSetting(Base):
    __tablename__ = "withdrawal_limit_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False, unique=True)
    daily_limit_amount = Column(Float, nullable=False, default=1000.0)
    current_daily_withdrawn = Column(Float, nullable=False, default=0.0)
    last_reset_date = Column(Date, nullable=False, server_default=func.current_date())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
