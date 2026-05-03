from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class LoanCreate(BaseModel):
    lender_user_id: int
    borrower_user_id: int
    amount: float = Field(..., gt=0)
    due_date: datetime

class LoanResponse(LoanCreate):
    id: int
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoanRequestResponse(BaseModel):
    loan: LoanResponse
    impact: Dict[str, float]
