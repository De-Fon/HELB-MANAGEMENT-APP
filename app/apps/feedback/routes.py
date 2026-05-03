from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.feedback.schemas import FeedbackCreate, FeedbackResponse
from app.apps.feedback.service import FeedbackService
from app.apps.feedback.providers import get_feedback_service

router = APIRouter()

@router.post(
    "/submit",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit student feedback"
)
def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    service: FeedbackService = Depends(get_feedback_service)
):
    """
    Submits student feedback regarding inflation and additional comments.
    """
    return service.submit_feedback(db, data)
