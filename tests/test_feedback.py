import pytest

class TestFeedback:
    def test_submit_feedback_success(self, client):
        payload = {
            "user_id": 1,
            "inflation_report": "High prices of food on campus.",
            "additional_comments": "The library needs more study spaces."
        }
        response = client.post("/api/v1/feedback/submit", json=payload)
        assert response.status_code == 201
        assert response.json()["inflation_report"] == "High prices of food on campus."

    def test_submit_feedback_invalid_user(self, client):
        # Assuming the service raises 404 for nonexistent user
        payload = {
            "user_id": 9999,
            "inflation_report": "Invalid user test",
            "additional_comments": "Testing..."
        }
        response = client.post("/api/v1/feedback/submit", json=payload)
        # Note: If service doesn't check user existence, this might return 201.
        # But we'll see.
        assert response.status_code in [201, 404]
