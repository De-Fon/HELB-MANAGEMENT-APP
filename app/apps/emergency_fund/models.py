from sqlalchemy import Column, Integer, Float, DateTime, func
from app.core.database import Base

class EmergencyFund(Base):
    __tablename__ = "emergency_funds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False, unique=True)
    reserved_percentage = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    remaining_amount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
