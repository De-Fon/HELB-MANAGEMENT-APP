import pytest

class TestCounselling:
    def test_book_session_success(self, client):
        payload = {
            "user_id": 1,
            "session_type": "money_management",
            "scheduled_date": "2026-06-01T10:00:00"
        }
        response = client.post("/api/v1/counselling/book", json=payload)
        assert response.status_code == 201
        assert response.json()["session_type"] == "money_management"

    def test_book_session_invalid_type(self, client):
        payload = {
            "user_id": 1,
            "session_type": "unknown_type",
            "scheduled_date": "2026-06-01T10:00:00"
        }
        response = client.post("/api/v1/counselling/book", json=payload)
        assert response.status_code == 400
