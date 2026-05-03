from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.scholarship_tracker.schemas import ScholarshipResponse
from app.apps.scholarship_tracker.service import ScholarshipService
from app.apps.scholarship_tracker.providers import get_scholarship_service
from app.apps.request_control.dependencies import idempotent, rate_limit
from app.apps.request_control.providers import get_request_control_service
from app.apps.request_control.service import RequestControlService

router = APIRouter()

@router.get(
    "/eligible",
    response_model=List[ScholarshipResponse],
    status_code=status.HTTP_200_OK,
    summary="Get eligible scholarships"
)
@rate_limit(max_requests=30, window_seconds=60)
def get_eligible_scholarships(
    request: Request,
    db: Session = Depends(get_db),
    service: ScholarshipService = Depends(get_scholarship_service),
    rc_service: RequestControlService = Depends(get_request_control_service)
):
    """
    Returns scholarships the user is eligible for.
    """
    user_profile_data = dict(request.query_params)
    return service.get_eligible_scholarships(db, user_profile_data)
