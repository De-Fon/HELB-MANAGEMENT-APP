from sqlalchemy import Column, Integer, String, Float, Text, Date
from app.core.database import Base

class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    deadline = Column(Date, nullable=False)
    eligibility_criteria = Column(Text, nullable=False)
    application_url = Column(String, nullable=False)
