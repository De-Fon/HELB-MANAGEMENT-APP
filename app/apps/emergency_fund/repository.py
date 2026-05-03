from sqlalchemy.orm import Session
from app.apps.emergency_fund.models import EmergencyFund

class EmergencyFundRepository:
    def get_fund(self, db: Session, user_id: int) -> EmergencyFund:
        return db.query(EmergencyFund).filter(EmergencyFund.user_id == user_id).first()

    def get_fund_for_update(self, db: Session, user_id: int) -> EmergencyFund:
        return db.query(EmergencyFund).filter(EmergencyFund.user_id == user_id).with_for_update().first()

    def update_fund_balance(self, db: Session, user_id: int, new_balance: float) -> EmergencyFund:
        fund = self.get_fund(db, user_id)
        if fund:
            fund.remaining_amount = new_balance
            db.flush()
            db.refresh(fund)
        return fund
