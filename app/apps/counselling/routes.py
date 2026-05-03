from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.counselling.schemas import CounsellingBookingCreate, CounsellingBookingResponse
from app.apps.counselling.service import CounsellingService
from app.apps.counselling.providers import get_counselling_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

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
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Books a counselling session for either money management or relationship advice.
    """
    return service.book_session(db, data)
