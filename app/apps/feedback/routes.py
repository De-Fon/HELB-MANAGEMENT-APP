from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.feedback.schemas import FeedbackCreate, FeedbackResponse
from app.apps.feedback.service import FeedbackService
from app.apps.feedback.providers import get_feedback_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

router = APIRouter()

@router.post(
    "/submit",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit student feedback"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def submit_feedback(
    request: Request,
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    service: FeedbackService = Depends(get_feedback_service),
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Submits student feedback regarding inflation and additional comments.
    """
    return service.submit_feedback(db, data)
