import pytest

class TestOfflineSync:
    def test_sync_queued_actions_success(self, client, db_session):
        # Create a queued action
        from app.apps.offline_sync.models import OfflineQueue
        q = OfflineQueue(user_id=1, endpoint="/api/v1/test", payload={"key": "val"})
        db_session.add(q)
        db_session.commit()

        response = client.post("/api/v1/offline/sync?user_id=1")
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1
        assert body[0]["sync_status"] == "synced"
