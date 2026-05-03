from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.apps.expenditure_analytics.models import ExpenditureSnapshot

class ExpenditureAnalyticsRepository:
    def get_user_expenditure_by_month(self, db: Session, user_id: int, month: int, year: int) -> List[ExpenditureSnapshot]:
        return db.query(ExpenditureSnapshot).filter(
            ExpenditureSnapshot.user_id == user_id,
            ExpenditureSnapshot.month == month,
            ExpenditureSnapshot.year == year
        ).all()

    def get_global_average_by_category(self, db: Session, month: int, year: int) -> dict:
        results = db.query(
            ExpenditureSnapshot.category, 
            func.avg(ExpenditureSnapshot.amount_spent).label('avg_amount')
        ).filter(
            ExpenditureSnapshot.month == month,
            ExpenditureSnapshot.year == year
        ).group_by(ExpenditureSnapshot.category).all()
        
        # Guard against None from avg()
        return {cat: round(avg, 2) if avg else 0.0 for cat, avg in results}
