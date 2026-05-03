from sqlalchemy import Column, Integer, String, DateTime, func, JSON
from app.core.database import Base

class OfflineQueue(Base):
    __tablename__ = "offline_queue"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    endpoint = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    synced_at = Column(DateTime(timezone=True), nullable=True)
