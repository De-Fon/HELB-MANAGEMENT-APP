from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class CounsellingSession(Base):
    __tablename__ = "counselling_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    session_type = Column(String, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
