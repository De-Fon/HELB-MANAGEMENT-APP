from fastapi import Depends
from app.apps.feedback.repository import FeedbackRepository
from app.apps.feedback.service import FeedbackService

def get_feedback_repository() -> FeedbackRepository:
    return FeedbackRepository()

def get_feedback_service(
    repo: FeedbackRepository = Depends(get_feedback_repository)
) -> FeedbackService:
    return FeedbackService(repository=repo)
