import pytest
from datetime import datetime

class TestMpesaIntegration:
    def test_sync_transactions_bulk(self, client):
        payload = {
            "user_id": 1,
            "transactions": [
                {
                    "user_id": 1,
                    "transaction_id": "TXN001",
                    "amount": 100.0,
                    "transaction_type": "paybill",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "user_id": 1,
                    "transaction_id": "TXN002",
                    "amount": 200.0,
                    "transaction_type": "buygoods",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        response = client.post("/api/v1/mpesa/sync", json=payload)
        assert response.status_code == 201
        assert len(response.json()) == 2

    def test_sync_duplicate_transaction(self, client):
        now = datetime.now().isoformat()
        payload = {
            "user_id": 1,
            "transactions": [
                {
                    "user_id": 1,
                    "transaction_id": "TXN003",
                    "amount": 100.0,
                    "transaction_type": "paybill",
                    "timestamp": now
                }
            ]
        }
        # First sync
        client.post("/api/v1/mpesa/sync", json=payload)
        
        # Second sync with same ID
        response = client.post("/api/v1/mpesa/sync", json=payload)
        assert response.status_code == 201
        assert len(response.json()) == 0 # Should ignore duplicates
