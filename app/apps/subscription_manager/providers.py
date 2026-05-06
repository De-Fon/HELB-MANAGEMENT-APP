from fastapi import Depends
from app.apps.subscription_manager.repository import SubscriptionRepository
from app.apps.subscription_manager.service import SubscriptionService
from app.apps.idempotency.providers import get_idempotency_service

def get_subscription_repository() -> SubscriptionRepository:
    return SubscriptionRepository()

def get_subscription_service(
    repo: SubscriptionRepository = Depends(get_subscription_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True)
) -> SubscriptionService:
    return SubscriptionService(
        repository=repo,
        idempotency_service=idempotency_service
    )
