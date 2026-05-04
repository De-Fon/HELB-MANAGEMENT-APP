from sqlalchemy.orm import Session
from datetime import date
from typing import List, Dict, Any
from app.apps.scholarship_tracker.repository import ScholarshipRepository
from app.apps.scholarship_tracker.models import Scholarship

class ScholarshipService:
    def __init__(
        self, 
        repository: ScholarshipRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def get_eligible_scholarships(self, db: Session, user_profile_data: Dict[str, Any]) -> List[Scholarship]:
        today = date.today()
        open_scholarships = self.repository.get_open_scholarships(db, today)
        
        # In a real app, filtering would happen here based on user_profile_data matching eligibility_criteria
        for sch in open_scholarships:
            sch.days_until_deadline = (sch.deadline - today).days
            
        return open_scholarships
