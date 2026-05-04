from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class IdempotencyRecordSchema(BaseModel):
    id: int
    idempotency_key: str
    user_id: int
    endpoint: str
    status_code: int
    response_body: Any
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True

class IdempotencyCheck(BaseModel):
    idempotency_key: str
    user_id: int
    endpoint: str
