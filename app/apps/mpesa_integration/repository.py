from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.apps.mpesa_integration.models import MpesaTransaction
from app.apps.mpesa_integration.schemas import MpesaTransactionImport
from typing import List

class MpesaTransactionRepository:
    def bulk_upsert_transactions(self, db: Session, user_id: int, txns_data: List[MpesaTransactionImport]) -> List[MpesaTransaction]:
        """
        Performs bulk import with 'ON CONFLICT DO NOTHING'.
        Filters for the specific user_id to ensure data integrity at the query level.
        """
        if not txns_data:
            return []
            
        # Filter for user_id and convert to dicts
        values = [
            txn.model_dump() 
            for txn in txns_data 
            if txn.user_id == user_id
        ]
        
        if not values:
            return []

        stmt = insert(MpesaTransaction).values(values)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=['transaction_id']
        ).returning(MpesaTransaction)
        
        result = db.execute(stmt)
        db.flush()
        return result.scalars().all()
