from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limiting import limiter
from app.apps.counselling.schemas import CounsellingBookingCreate, CounsellingBookingResponse
from app.apps.counselling.service import CounsellingService
from app.apps.counselling.providers import get_counselling_service
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post(
    "/book",
    response_model=CounsellingBookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Book a counselling session"
)
@idempotent()
@limiter.limit("5/minute")
def book_session(
    request: Request,
    response: Response,
    data: CounsellingBookingCreate,
    db: Session = Depends(get_db),
    service: CounsellingService = Depends(get_counselling_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    """
    Books a counselling session for either money management or relationship advice.
    """
    return service.book_session(db, data)
