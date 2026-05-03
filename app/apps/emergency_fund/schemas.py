from pydantic import BaseModel, Field

class EmergencyFundSetup(BaseModel):
    user_id: int
    reserved_percentage: float = Field(..., ge=0, le=100)

class EmergencyFundResponse(BaseModel):
    user_id: int
    total_amount: float
    remaining_amount: float
    reserved_percentage: float

    class Config:
        from_attributes = True

class EmergencyFundWithdraw(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0)
