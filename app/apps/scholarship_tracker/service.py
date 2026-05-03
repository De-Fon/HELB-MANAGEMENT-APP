from sqlalchemy.orm import Session
from datetime import date
from typing import List, Dict, Any
from app.apps.scholarship_tracker.repository import ScholarshipRepository

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

    def get_eligible_scholarships(self, db: Session, user_profile_data: Dict[str, Any]) -> List[Dict]:
        today = date.today()
        open_scholarships = self.repository.get_open_scholarships(db, today)
        
        eligible = []
        # In a real app, filtering would happen here based on user_profile_data matching eligibility_criteria
        for sch in open_scholarships:
            days_until = (sch.deadline - today).days
            eligible.append({
                "id": sch.id,
                "name": sch.name,
                "provider": sch.provider,
                "amount": sch.amount,
                "deadline": sch.deadline,
                "eligibility_criteria": sch.eligibility_criteria,
                "application_url": sch.application_url,
                "days_until_deadline": days_until
            })
            
        return eligible
