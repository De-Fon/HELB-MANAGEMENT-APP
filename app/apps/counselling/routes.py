from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.apps.counselling.schemas import CounsellingBookingCreate, CounsellingBookingResponse
from app.apps.counselling.service import CounsellingService
from app.apps.counselling.providers import get_counselling_service

router = APIRouter()

@router.post(
    "/book",
    response_model=CounsellingBookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Book a counselling session"
)
def book_session(
    data: CounsellingBookingCreate,
    db: Session = Depends(get_db),
    service: CounsellingService = Depends(get_counselling_service)
):
    """
    Books a counselling session for either money management or relationship advice.
    """
    return service.book_session(db, data)
