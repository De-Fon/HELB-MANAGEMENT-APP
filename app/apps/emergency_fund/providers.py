from fastapi import Depends
from app.apps.emergency_fund.repository import EmergencyFundRepository
from app.apps.emergency_fund.service import EmergencyFundService

def get_emergency_fund_repository() -> EmergencyFundRepository:
    return EmergencyFundRepository()

def get_emergency_fund_service(
    repo: EmergencyFundRepository = Depends(get_emergency_fund_repository)
) -> EmergencyFundService:
    return EmergencyFundService(repository=repo)
