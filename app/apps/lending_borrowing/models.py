from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    lender_user_id = Column(Integer, index=True, nullable=False)
    borrower_user_id = Column(Integer, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pending")
    due_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
