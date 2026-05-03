import pytest

class TestLendingBorrowing:
    def test_request_loan_success(self, client):
        payload = {
            "lender_user_id": 1,
            "borrower_user_id": 2,
            "amount": 500.0,
            "due_date": "2026-12-31T23:59:59"
        }
        response = client.post("/api/v1/lending-borrowing/request", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["impact"]["user_1_balance_change"] == -500.0
        assert body["impact"]["user_2_balance_change"] == 500.0
