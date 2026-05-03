from sqlalchemy.orm import Session
from datetime import date
from typing import List, Dict
from app.apps.subscription_manager.repository import SubscriptionRepository

class SubscriptionService:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository

    def check_and_alert_renewals(self, db: Session, user_id: int) -> List[Dict]:
        upcoming = self.repository.get_upcoming_renewals(db, user_id, days_ahead=7)
        alerts = []
        today = date.today()
        
        for sub in upcoming:
            days_until = (sub.renewal_date - today).days
            alerts.append({
                "id": sub.id,
                "user_id": sub.user_id,
                "service_name": sub.service_name,
                "amount": sub.amount,
                "renewal_date": sub.renewal_date,
                "is_active": sub.is_active,
                "auto_renew": sub.auto_renew,
                "days_until_renewal": days_until
            })
            
        return alerts
