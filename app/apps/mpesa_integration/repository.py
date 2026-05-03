from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.apps.mpesa_integration.models import MpesaTransaction
from app.apps.mpesa_integration.schemas import MpesaTransactionImport
from typing import List

class MpesaTransactionRepository:
    def bulk_import_transactions(self, db: Session, txns_data: List[MpesaTransactionImport]) -> List[MpesaTransaction]:
        if not txns_data:
            return []
            
        stmt = insert(MpesaTransaction).values([txn.model_dump() for txn in txns_data])
        stmt = stmt.on_conflict_do_nothing(index_elements=['transaction_id']).returning(MpesaTransaction)
        
        result = db.execute(stmt)
        db.flush()
        return result.scalars().all()
