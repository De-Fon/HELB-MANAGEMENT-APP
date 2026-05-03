from sqlalchemy.orm import Session
from datetime import date
from typing import List
from app.apps.scholarship_tracker.models import Scholarship

class ScholarshipRepository:
    def get_open_scholarships(self, db: Session, current_date: date) -> List[Scholarship]:
        return db.query(Scholarship).filter(Scholarship.deadline >= current_date).all()
