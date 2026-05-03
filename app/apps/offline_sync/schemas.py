from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime

class OfflineActionCreate(BaseModel):
    user_id: int
    endpoint: str
    payload: Dict[str, Any]

class OfflineQueueResponse(OfflineActionCreate):
    id: int
    created_at: Optional[datetime] = None
    synced_at: Optional[datetime] = None
    sync_status: str

    class Config:
        from_attributes = True
