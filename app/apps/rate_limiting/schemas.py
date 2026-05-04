from pydantic import BaseModel
from datetime import datetime

class RateLimitResponse(BaseModel):
    user_id: int
    endpoint: str
    request_count: int
    window_start: datetime
    window_end: datetime

    class Config:
        from_attributes = True
