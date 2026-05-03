from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FeedbackBase(BaseModel):
    user_id: int
    inflation_report: str = Field(..., description="Report on how inflation has affected the student")
    additional_comments: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    submitted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
