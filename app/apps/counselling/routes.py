from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.counselling.schemas import CounsellingBookingCreate, CounsellingBookingResponse
from app.apps.counselling.service import CounsellingService
from app.apps.counselling.providers import get_counselling_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.post(
    "/book",
    response_model=CounsellingBookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Book a counselling session"
)
@idempotent()
@rate_limit(max_requests=5, window_seconds=60)
def book_session(
    request: Request,
    data: CounsellingBookingCreate,
    db: Session = Depends(get_db),
    service: CounsellingService = Depends(get_counselling_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    """
    Books a counselling session for either money management or relationship advice.
    """
    return service.book_session(db, data)
