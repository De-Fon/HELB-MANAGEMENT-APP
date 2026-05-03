from sqlalchemy.orm import Session
from app.apps.emergency_fund.models import EmergencyFund

class EmergencyFundRepository:
    def get_fund(self, db: Session, user_id: int) -> EmergencyFund:
        """Fetch fund without locking."""
        return db.query(EmergencyFund).filter(EmergencyFund.user_id == user_id).first()

    def get_fund_for_update(self, db: Session, user_id: int) -> EmergencyFund:
        """Fetch fund with row-level locking to prevent race conditions."""
        return db.query(EmergencyFund).filter(EmergencyFund.user_id == user_id).with_for_update().first()

    def update_balance(self, db: Session, fund: EmergencyFund, amount: float):
        """Update balance on an existing (potentially locked) fund object."""
        fund.remaining_amount = amount
        db.flush()
        return fund
