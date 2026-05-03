from pydantic import BaseModel, Field
from typing import Dict

class ExpenditureDataPoint(BaseModel):
    user_id: int
    category: str
    amount_spent: float = Field(..., ge=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., gt=2000)

class ExpenditureReport(BaseModel):
    user_id: int
    category_breakdown: Dict[str, float]
    total_spent: float
    peer_average_comparison: Dict[str, float]

    class Config:
        from_attributes = True
