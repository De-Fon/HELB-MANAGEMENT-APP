from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.emergency_fund.repository import EmergencyFundRepository
from app.apps.emergency_fund.models import EmergencyFund

class EmergencyFundService:
    def __init__(
        self, 
        repository: EmergencyFundRepository,
        idempotency_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
    def withdraw_from_emergency(self, db: Session, user_id: int, amount: float) -> EmergencyFund:
        """
        Withdraws from emergency fund. 
        Uses row-level locking via repository to prevent race conditions.
        """
        fund = self.repository.get_fund_for_update(db, user_id)
        if not fund:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emergency fund not found.")
            
        if amount > fund.remaining_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient emergency funds.")
            
        new_balance = fund.remaining_amount - amount
        self.repository.update_balance(db, fund, new_balance)
        
        db.commit()
        return fund
