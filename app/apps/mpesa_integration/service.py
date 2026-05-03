from sqlalchemy.orm import Session
from typing import List
from app.apps.mpesa_integration.repository import MpesaTransactionRepository
from app.apps.mpesa_integration.schemas import MpesaTransactionImport

class MpesaTransactionService:
    def __init__(self, repository: MpesaTransactionRepository):
        self.repository = repository

    def sync_transactions(self, db: Session, user_id: int, transaction_list: List[MpesaTransactionImport]):
        # Deduplicate list by transaction_id in memory first
        seen_txns = set()
        unique_txns = []
        for txn in transaction_list:
            if txn.transaction_id not in seen_txns and txn.user_id == user_id:
                seen_txns.add(txn.transaction_id)
                unique_txns.append(txn)
                
        imported = self.repository.bulk_import_transactions(db, unique_txns)
        db.commit()
        return imported
