from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BudgetAllocationBase(BaseModel):
    user_id: int
    semester_start: datetime
    semester_end: datetime
    total_helb_amount: float = Field(..., gt=0)
    rent_allocation: float = Field(..., ge=0)
    food_allocation: float = Field(..., ge=0)
    transport_allocation: float = Field(..., ge=0)
    personal_needs_allocation: float = Field(..., ge=0)

class BudgetAllocationCreate(BudgetAllocationBase):
    pass

class BudgetAllocationResponse(BudgetAllocationBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
