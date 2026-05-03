from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

class MpesaTransaction(Base):
    __tablename__ = "mpesa_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    imported_at = Column(DateTime(timezone=True), server_default=func.now())
