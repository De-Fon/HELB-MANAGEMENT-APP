from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class ExpenditureSnapshot(Base):
    __tablename__ = "expenditure_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    amount_spent = Column(Float, nullable=False)
    month = Column(Integer, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
