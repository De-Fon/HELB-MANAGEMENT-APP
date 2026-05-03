"""
test_budget_tracker.py - Tests for /api/v1/budget-tracker endpoints.

Covers:
- POST /allocate: success, exceeds HELB total, missing fields
"""
import pytest
from datetime import datetime, timedelta


def valid_payload(
    user_id=1,
    total_helb_amount=50000.0,
    rent=20000.0,
    food=10000.0,
    transport=5000.0,
    personal=5000.0,
):
    """Helper that builds a valid BudgetAllocationCreate payload."""
    now = datetime.utcnow()
    return {
        "user_id": user_id,
        "semester_start": now.isoformat(),
        "semester_end": (now + timedelta(days=120)).isoformat(),
        "total_helb_amount": total_helb_amount,
        "rent_allocation": rent,
        "food_allocation": food,
        "transport_allocation": transport,
        "personal_needs_allocation": personal,
    }


class TestBudgetAllocate:
    def test_allocate_success(self, client):
        """A valid budget allocation is created successfully."""
        response = client.post("/api/v1/budget-tracker/allocate", json=valid_payload())
        assert response.status_code == 201
        body = response.json()
        assert body["user_id"] == 1
        assert body["total_helb_amount"] == 50000.0
        assert "id" in body

    def test_allocate_exceeds_total(self, client):
        """Allocations exceeding the total HELB amount return 400."""
        # Allocations sum to 50000 but HELB total is only 30000
        payload = valid_payload(
            total_helb_amount=30000.0,
            rent=20000.0,
            food=15000.0,    # total: 50000 > 30000
            transport=5000.0,
            personal=10000.0,
        )
        response = client.post("/api/v1/budget-tracker/allocate", json=payload)
        assert response.status_code == 400
        assert "exceed" in response.json()["detail"].lower()

    def test_allocate_exact_total(self, client):
        """Allocations exactly equal to the HELB total are accepted."""
        payload = valid_payload(
            total_helb_amount=40000.0,
            rent=20000.0,
            food=10000.0,
            transport=5000.0,
            personal=5000.0,  # sum = 40000.0 exactly
        )
        response = client.post("/api/v1/budget-tracker/allocate", json=payload)
        assert response.status_code == 201

    def test_allocate_missing_required_field(self, client):
        """Missing a required field returns a 422 validation error."""
        payload = valid_payload()
        del payload["total_helb_amount"]
        response = client.post("/api/v1/budget-tracker/allocate", json=payload)
        assert response.status_code == 422

    def test_allocate_negative_helb_amount(self, client):
        """A HELB amount of zero or negative is rejected by schema validation."""
        payload = valid_payload(total_helb_amount=0)
        response = client.post("/api/v1/budget-tracker/allocate", json=payload)
        assert response.status_code == 422
