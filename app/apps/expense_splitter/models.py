from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.database import Base

class SharedExpense(Base):
    __tablename__ = "shared_expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, index=True, nullable=False)
    paid_by_user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    split_among_user_ids = Column(ARRAY(Integer), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
