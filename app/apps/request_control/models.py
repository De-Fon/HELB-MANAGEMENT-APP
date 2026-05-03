from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, func
from app.core.database import Base
from datetime import datetime, timedelta

class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    id = Column(Integer, primary_key=True, index=True)
    idempotency_key = Column(String, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    endpoint = Column(String, index=True, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_body = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

class RateLimitRecord(Base):
    __tablename__ = "rate_limit_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    endpoint = Column(String, index=True, nullable=False)
    request_count = Column(Integer, default=1)
    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)
