from sqlalchemy.orm import Session
from datetime import timedelta, date
from typing import List
from app.apps.subscription_manager.models import Subscription

class SubscriptionRepository:
    def get_upcoming_renewals(self, db: Session, user_id: int, days_ahead: int = 7) -> List[Subscription]:
        today = date.today()
        upcoming_date = today + timedelta(days=days_ahead)
        return db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.is_active == True,
            Subscription.renewal_date >= today,
            Subscription.renewal_date <= upcoming_date
        ).all()
