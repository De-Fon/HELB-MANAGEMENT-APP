from sqlalchemy.orm import Session
from app.apps.feedback.models import StudentFeedback
from app.apps.feedback.schemas import FeedbackCreate

class FeedbackRepository:
    def create_feedback(self, db: Session, data: FeedbackCreate) -> StudentFeedback:
        db_feedback = StudentFeedback(**data.model_dump())
        db.add(db_feedback)
        db.flush()
        db.refresh(db_feedback)
        return db_feedback
