from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

class BudgetAllocation(Base):
    __tablename__ = "budget_allocations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False) # Assuming integer user ID
    semester_start = Column(DateTime, nullable=False)
    semester_end = Column(DateTime, nullable=False)
    total_helb_amount = Column(Float, nullable=False)
    rent_allocation = Column(Float, nullable=False)
    food_allocation = Column(Float, nullable=False)
    transport_allocation = Column(Float, nullable=False)
    personal_needs_allocation = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
