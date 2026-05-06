from fastapi import Depends
from app.apps.feedback.repository import FeedbackRepository
from app.apps.feedback.service import FeedbackService
from app.apps.idempotency.providers import get_idempotency_service

def get_feedback_repository() -> FeedbackRepository:
    return FeedbackRepository()

def get_feedback_service(
    repo: FeedbackRepository = Depends(get_feedback_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True)
) -> FeedbackService:
    return FeedbackService(
        repository=repo,
        idempotency_service=idempotency_service
    )
