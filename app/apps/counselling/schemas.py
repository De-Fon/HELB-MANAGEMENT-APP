from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CounsellingBookingBase(BaseModel):
    user_id: int
    session_type: str = Field(..., description="Type of session: money_management or relationship_advice")
    scheduled_date: datetime

class CounsellingBookingCreate(CounsellingBookingBase):
    pass

class CounsellingBookingResponse(CounsellingBookingBase):
    id: int
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
