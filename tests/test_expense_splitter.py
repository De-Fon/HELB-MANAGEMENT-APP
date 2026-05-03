import pytest

class TestExpenseSplitter:
    def test_split_expense_success(self, client):
        payload = {
            "group_id": 101,
            "paid_by_user_id": 1,
            "amount": 300.0,
            "description": "Dinner",
            "split_among_user_ids": [1, 2, 3]
        }
        response = client.post("/api/v1/expense-splitter/add", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["calculated_balance_per_user"]["2"] == 100.0
        assert body["calculated_balance_per_user"]["3"] == 100.0
        assert body["calculated_balance_per_user"]["1"] == 0.0

    def test_split_expense_empty_users(self, client):
        payload = {
            "group_id": 101,
            "paid_by_user_id": 1,
            "amount": 300.0,
            "description": "Dinner",
            "split_among_user_ids": []
        }
        response = client.post("/api/v1/expense-splitter/add", json=payload)
        assert response.status_code == 400
