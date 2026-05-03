from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class SharedExpenseCreate(BaseModel):
    group_id: int
    paid_by_user_id: int
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    split_among_user_ids: List[int]

class SharedExpenseResponse(SharedExpenseCreate):
    id: int
    created_at: Optional[datetime] = None
    calculated_balance_per_user: Dict[int, float]

    class Config:
        from_attributes = True
