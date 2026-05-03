from pydantic import BaseModel, Field
from datetime import date

class ScholarshipCreate(BaseModel):
    name: str
    provider: str
    amount: float = Field(..., gt=0)
    deadline: date
    eligibility_criteria: str
    application_url: str

class ScholarshipResponse(ScholarshipCreate):
    id: int
    days_until_deadline: int

    class Config:
        from_attributes = True
