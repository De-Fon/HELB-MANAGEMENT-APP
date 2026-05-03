from fastapi import Depends
from app.apps.subscription_manager.repository import SubscriptionRepository
from app.apps.subscription_manager.service import SubscriptionService

def get_subscription_repository() -> SubscriptionRepository:
    return SubscriptionRepository()

def get_subscription_service(
    repo: SubscriptionRepository = Depends(get_subscription_repository)
) -> SubscriptionService:
    return SubscriptionService(repository=repo)
