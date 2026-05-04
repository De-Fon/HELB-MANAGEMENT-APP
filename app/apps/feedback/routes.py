from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.feedback.schemas import FeedbackCreate, FeedbackResponse
from app.apps.feedback.service import FeedbackService
from app.apps.feedback.providers import get_feedback_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

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
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Submits student feedback regarding inflation and additional comments.
    """
    return service.submit_feedback(db, data)
