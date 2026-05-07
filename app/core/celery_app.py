import os
from celery import Celery
from app.core.config import settings

# Create the Celery instance
# 'app' is the name of the main module (app/)
celery_app = Celery(
    "helb_backend",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # This automatically finds tasks.py in your app/apps/*/ modules
    task_track_started=True,
    task_time_limit=30 * 60, # 30 minutes
)

# Auto-discover tasks in all feature modules
# Celery will look for 'tasks.py' inside any package listed here
celery_app.autodiscover_tasks([
    "app.apps.auth",
    "app.apps.budget_tracker",
    "app.apps.counselling",
    "app.apps.emergency_fund",
    "app.apps.expenditure_analytics",
    "app.apps.expense_splitter",
    "app.apps.feedback",
    "app.apps.lending_borrowing",
    "app.apps.mpesa_integration",
    "app.apps.offline_sync",
    "app.apps.scholarship_tracker",
    "app.apps.subscription_manager",
    "app.apps.withdrawal_limit",
])
