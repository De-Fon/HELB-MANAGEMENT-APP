from sqlalchemy.orm import Session
from app.apps.expenditure_analytics.repository import ExpenditureAnalyticsRepository
from app.apps.expenditure_analytics.schemas import ExpenditureReport

class ExpenditureAnalyticsService:
    def __init__(
        self, 
        repository: ExpenditureAnalyticsRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def generate_comparison_report(self, db: Session, user_id: int, month: int, year: int) -> ExpenditureReport:
        """
        Generates a comparison report. 
        Business logic handles the delta calculation between user totals and peer averages.
        """
        category_breakdown = self.repository.get_category_totals(db, user_id, month, year)
        peer_averages = self.repository.get_global_averages(db, month, year)
        
        total_spent = sum(category_breakdown.values())
        
        peer_average_comparison = {}
        # Ensure we compare all categories the user has spent in
        for cat, spent in category_breakdown.items():
            avg = peer_averages.get(cat, 0.0)
            peer_average_comparison[cat] = round(spent - avg, 2)
            
        return ExpenditureReport(
            user_id=user_id,
            category_breakdown=category_breakdown,
            total_spent=total_spent,
            peer_average_comparison=peer_average_comparison
        )
