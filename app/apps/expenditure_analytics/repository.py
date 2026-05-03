from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
from app.apps.expenditure_analytics.models import ExpenditureSnapshot

class ExpenditureAnalyticsRepository:
    def get_category_totals(self, db: Session, user_id: int, month: int, year: int) -> Dict[str, float]:
        """Aggregate user expenditures by category in the database."""
        results = db.query(
            ExpenditureSnapshot.category,
            func.sum(ExpenditureSnapshot.amount_spent).label('total')
        ).filter(
            ExpenditureSnapshot.user_id == user_id,
            ExpenditureSnapshot.month == month,
            ExpenditureSnapshot.year == year
        ).group_by(ExpenditureSnapshot.category).all()
        
        return {cat: float(total) for cat, total in results}

    def get_global_averages(self, db: Session, month: int, year: int) -> Dict[str, float]:
        """Calculate global averages by category in the database."""
        results = db.query(
            ExpenditureSnapshot.category, 
            func.avg(ExpenditureSnapshot.amount_spent).label('avg_amount')
        ).filter(
            ExpenditureSnapshot.month == month,
            ExpenditureSnapshot.year == year
        ).group_by(ExpenditureSnapshot.category).all()
        
        return {cat: round(float(avg), 2) if avg else 0.0 for cat, avg in results}
