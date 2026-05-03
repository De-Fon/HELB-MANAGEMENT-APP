from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class StudentFeedback(Base):
    __tablename__ = "student_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    inflation_report = Column(String, nullable=False)
    additional_comments = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
