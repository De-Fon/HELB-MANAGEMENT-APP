from fastapi import Depends
from app.apps.request_control.repository import RequestControlRepository
from app.apps.request_control.service import RequestControlService

def get_request_control_repository() -> RequestControlRepository:
    return RequestControlRepository()

def get_request_control_service(
    repo: RequestControlRepository = Depends(get_request_control_repository)
) -> RequestControlService:
    return RequestControlService(repository=repo)

# Aliases requested by the user
def get_idempotency_service(
    service: RequestControlService = Depends(get_request_control_service)
) -> RequestControlService:
    return service

def get_rate_limit_service(
    service: RequestControlService = Depends(get_request_control_service)
) -> RequestControlService:
    return service
