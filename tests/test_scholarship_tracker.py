import pytest
from datetime import datetime

class TestScholarshipTracker:
    def test_get_eligible_scholarships(self, client, db_session):
        # Setup test data
        from app.apps.scholarship_tracker.models import Scholarship
        from datetime import date
        s = Scholarship(
            name="STEM", 
            provider="Gov", 
            amount=1000.0, 
            deadline=date.today(), 
            eligibility_criteria="GPA > 3.5",
            application_url="http://example.com"
        )
        db_session.add(s)
        db_session.flush()

        response = client.get("/api/v1/scholarships/eligible?gpa=3.8")
        assert response.status_code == 200
        assert len(response.json()) >= 1
