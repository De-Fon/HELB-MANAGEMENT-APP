from sqlalchemy.orm import Session
from app.apps.expenditure_analytics.repository import ExpenditureAnalyticsRepository
from app.apps.expenditure_analytics.schemas import ExpenditureReport

class ExpenditureAnalyticsService:
    def __init__(self, repository: ExpenditureAnalyticsRepository):
        self.repository = repository

    def generate_comparison_report(self, db: Session, user_id: int, month: int, year: int) -> ExpenditureReport:
        user_data = self.repository.get_user_expenditure_by_month(db, user_id, month, year)
        
        category_breakdown = {}
        total_spent = 0.0
        
        for record in user_data:
            cat = record.category
            category_breakdown[cat] = category_breakdown.get(cat, 0.0) + record.amount_spent
            total_spent += record.amount_spent
            
        peer_averages = self.repository.get_global_average_by_category(db, month, year)
        
        peer_average_comparison = {}
        for cat, spent in category_breakdown.items():
            avg = peer_averages.get(cat, 0.0)
            peer_average_comparison[cat] = spent - avg
            
        return ExpenditureReport(
            user_id=user_id,
            category_breakdown=category_breakdown,
            total_spent=total_spent,
            peer_average_comparison=peer_average_comparison
        )
