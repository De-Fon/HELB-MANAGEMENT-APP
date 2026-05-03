from pydantic import BaseModel
from typing import Any, Optional

class IdempotencyCheck(BaseModel):
    idempotency_key: str
    user_id: int
    endpoint: str

class IdempotencyResponse(BaseModel):
    idempotency_key: str
    was_cached: bool
    cached_response: Optional[Any] = None
