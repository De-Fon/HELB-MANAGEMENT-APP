import pytest
from datetime import datetime, timedelta

class TestSubscriptionManager:
    def test_get_upcoming_renewals(self, client, db_session):
        from app.apps.subscription_manager.models import Subscription
        from datetime import date, timedelta
        today = date.today()
        renewal = today + timedelta(days=2)
        s = Subscription(user_id=1, service_name="spotify", amount=5.0, renewal_date=renewal)
        db_session.add(s)
        db_session.commit()

        response = client.get("/api/v1/subscriptions/upcoming/1")
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["service_name"] == "spotify"
