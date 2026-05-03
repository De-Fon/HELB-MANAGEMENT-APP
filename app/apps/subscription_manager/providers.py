from fastapi import Depends
from app.apps.subscription_manager.repository import SubscriptionRepository
from app.apps.subscription_manager.service import SubscriptionService
from app.apps.request_control.providers import get_idempotency_service, get_rate_limit_service

def get_subscription_repository() -> SubscriptionRepository:
    return SubscriptionRepository()

def get_subscription_service(
    repo: SubscriptionRepository = Depends(get_subscription_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> SubscriptionService:
    return SubscriptionService(
        repository=repo,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )
