from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.feedback.repository import FeedbackRepository
from app.apps.feedback.schemas import FeedbackCreate
from app.apps.feedback.models import StudentFeedback

class FeedbackService:
    def __init__(
        self, 
        repository: FeedbackRepository,
        idempotency_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
    def submit_feedback(self, db: Session, data: FeedbackCreate) -> StudentFeedback:
        # Validate user_id exists
        # Note: In a complete system, this would query the UserRepository.
        # Since we don't have a users table yet, we perform a basic validation.
        if data.user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        feedback = self.repository.create_feedback(db, data)
        db.commit()
        return feedback
