from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.core.database import Base
from app.shared.utils import get_current_utc_time

class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    id = Column(Integer, primary_key=True, index=True)
    idempotency_key = Column(String, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    endpoint = Column(String, index=True, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_body = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_current_utc_time)
    expires_at = Column(DateTime(timezone=True), nullable=False)
