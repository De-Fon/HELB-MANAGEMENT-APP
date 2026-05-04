from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from app.shared.utils import get_current_utc_time

class RateLimitRecord(Base):
    __tablename__ = "rate_limit_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    endpoint = Column(String, index=True, nullable=False)
    request_count = Column(Integer, default=1)
    window_start = Column(DateTime(timezone=True), default=get_current_utc_time)
    window_end = Column(DateTime(timezone=True), nullable=False)
