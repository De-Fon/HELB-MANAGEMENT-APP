import pytest
from datetime import datetime

class TestExpenditureAnalytics:
    def test_get_summary(self, client, db_session):
        # Setup test snapshots
        from app.apps.expenditure_analytics.models import ExpenditureSnapshot
        now = datetime.now()
        s1 = ExpenditureSnapshot(user_id=1, category="food", amount_spent=150.0, month=now.month, year=now.year)
        s2 = ExpenditureSnapshot(user_id=1, category="rent", amount_spent=1000.0, month=now.month, year=now.year)
        db_session.add_all([s1, s2])
        db_session.flush()

        response = client.get(f"/api/v1/expenditure-analytics/report/1?month={now.month}&year={now.year}")
        assert response.status_code == 200
        body = response.json()
        assert body["total_spent"] == 1150.0
        assert body["category_breakdown"]["food"] == 150.0
        assert body["category_breakdown"]["rent"] == 1000.0
