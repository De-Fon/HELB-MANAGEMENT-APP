from fastapi import Depends
from app.apps.counselling.repository import CounsellingRepository
from app.apps.counselling.service import CounsellingService

def get_counselling_repository() -> CounsellingRepository:
    return CounsellingRepository()

def get_counselling_service(
    repo: CounsellingRepository = Depends(get_counselling_repository)
) -> CounsellingService:
    return CounsellingService(repository=repo)
