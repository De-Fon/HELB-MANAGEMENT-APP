from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.feedback.schemas import FeedbackCreate, FeedbackResponse
from app.apps.feedback.service import FeedbackService
from app.apps.feedback.providers import get_feedback_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/submit",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit student feedback"
)
@idempotent()
@limiter.limit("5/minute")
def submit_feedback(
    request: Request,
    response: Response,
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    service: FeedbackService = Depends(get_feedback_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Submits student feedback regarding inflation and additional comments.
    """
    return service.submit_feedback(db, data)
