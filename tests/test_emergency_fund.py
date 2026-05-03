import pytest

class TestEmergencyFund:
    def test_withdraw_success(self, client, db_session):
        # Setup initial fund
        from app.apps.emergency_fund.models import EmergencyFund
        fund = EmergencyFund(user_id=1, reserved_percentage=10.0, total_amount=1000.0, remaining_amount=1000.0)
        db_session.add(fund)
        db_session.flush() # Use flush instead of commit to stay within the fixture transaction

        response = client.post("/api/v1/emergency-fund/withdraw", json={"user_id": 1, "amount": 200.0})
        assert response.status_code == 200
        assert response.json()["remaining_amount"] == 800.0

    def test_withdraw_insufficient_funds(self, client, db_session):
        from app.apps.emergency_fund.models import EmergencyFund
        fund = EmergencyFund(user_id=2, reserved_percentage=10.0, total_amount=100.0, remaining_amount=100.0)
        db_session.add(fund)
        db_session.flush()

        response = client.post("/api/v1/emergency-fund/withdraw", json={"user_id": 2, "amount": 200.0})
        assert response.status_code == 400
