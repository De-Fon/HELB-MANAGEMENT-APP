import pytest

class TestWithdrawalLimit:
    def test_check_eligibility_first_time(self, client):
        response = client.get("/api/v1/withdrawal-limit/1/check?amount=500.0")
        assert response.status_code == 200
        body = response.json()
        assert body["eligible"] is True
        assert body["remaining_today"] == 1000.0 # Initial limit is 1000

    def test_check_eligibility_exceed_limit(self, client):
        response = client.get("/api/v1/withdrawal-limit/1/check?amount=1500.0")
        assert response.status_code == 200
        assert response.json()["eligible"] is False
