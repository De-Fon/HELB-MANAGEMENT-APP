from pydantic import BaseModel, Field
from typing import Optional

class WithdrawalLimitCreate(BaseModel):
    user_id: int
    daily_limit_amount: float = Field(..., gt=0)

class WithdrawalLimitResponse(BaseModel):
    user_id: int
    daily_limit_amount: float
    current_daily_withdrawn: float
    remaining_today: float
    eligible: Optional[bool] = None

    class Config:
        from_attributes = True
