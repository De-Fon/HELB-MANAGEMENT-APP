from sqlalchemy.orm import Session
from typing import List
from app.apps.mpesa_integration.repository import MpesaTransactionRepository
from app.apps.mpesa_integration.schemas import MpesaTransactionImport

class MpesaTransactionService:
    def __init__(
        self, 
        repository: MpesaTransactionRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def sync_transactions(self, db: Session, user_id: int, transaction_list: List[MpesaTransactionImport]):
        """
        Syncs transactions by delegating deduplication and persistence to the repository.
        """
        imported = self.repository.bulk_upsert_transactions(db, user_id, transaction_list)
        db.commit()
        return imported
