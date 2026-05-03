from pydantic import BaseModel, Field
from datetime import date

class SubscriptionCreate(BaseModel):
    user_id: int
    service_name: str
    amount: float = Field(..., gt=0)
    renewal_date: date
    auto_renew: bool = True

class SubscriptionResponse(SubscriptionCreate):
    id: int
    is_active: bool
    days_until_renewal: int

    class Config:
        from_attributes = True
