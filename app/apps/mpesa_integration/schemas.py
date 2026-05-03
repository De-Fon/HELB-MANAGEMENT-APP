from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MpesaTransactionImport(BaseModel):
    user_id: int
    transaction_id: str
    amount: float
    transaction_type: str
    timestamp: datetime

class MpesaTransactionResponse(MpesaTransactionImport):
    id: int
    imported_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MpesaSyncRequest(BaseModel):
    user_id: int
    transactions: List[MpesaTransactionImport]
