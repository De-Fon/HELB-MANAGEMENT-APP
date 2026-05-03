from fastapi import Depends
from app.apps.scholarship_tracker.repository import ScholarshipRepository
from app.apps.scholarship_tracker.service import ScholarshipService

def get_scholarship_repository() -> ScholarshipRepository:
    return ScholarshipRepository()

def get_scholarship_service(
    repo: ScholarshipRepository = Depends(get_scholarship_repository)
) -> ScholarshipService:
    return ScholarshipService(repository=repo)
