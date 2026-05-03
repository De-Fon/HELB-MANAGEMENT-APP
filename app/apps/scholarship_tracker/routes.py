from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.apps.scholarship_tracker.schemas import ScholarshipResponse
from app.apps.scholarship_tracker.service import ScholarshipService
from app.apps.scholarship_tracker.providers import get_scholarship_service

router = APIRouter()

@router.get(
    "/eligible",
    response_model=List[ScholarshipResponse],
    status_code=status.HTTP_200_OK,
    summary="Get eligible scholarships"
)
def get_eligible_scholarships(
    request: Request,
    db: Session = Depends(get_db),
    service: ScholarshipService = Depends(get_scholarship_service)
):
    """
    Returns scholarships the user is eligible for.
    """
    user_profile_data = dict(request.query_params)
    return service.get_eligible_scholarships(db, user_profile_data)
