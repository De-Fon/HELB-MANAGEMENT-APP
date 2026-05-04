from fastapi import FastAPI
from app.core.settings import settings
from app.core.logging import setup_logging
from app.shared.middleware import RequestLoggingMiddleware

# ── 1. Initialise Loguru before anything else ────────────────────────────────
setup_logging()

from loguru import logger
logger.info(f"Starting {settings.PROJECT_NAME}...")

# ── 2. Create the FastAPI application ─────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)

# ── 3. Register middleware (runs before routes) ───────────────────────────────
app.add_middleware(RequestLoggingMiddleware)

# ── 4. Register global exception handlers ─────────────────────────────────────
from app.shared.exceptions import setup_exception_handlers
setup_exception_handlers(app)

# ── 5. Health check ───────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "project": settings.PROJECT_NAME}

# ── 6. Register all feature routers ──────────────────────────────────────────
from app.apps.budget_tracker.routes import router as budget_router
from app.apps.feedback.routes import router as feedback_router
from app.apps.counselling.routes import router as counselling_router
from app.apps.withdrawal_limit.routes import router as withdrawal_router
from app.apps.mpesa_integration.routes import router as mpesa_router
from app.apps.emergency_fund.routes import router as emergency_fund_router
from app.apps.expense_splitter.routes import router as expense_splitter_router
from app.apps.lending_borrowing.routes import router as lending_borrowing_router
from app.apps.expenditure_analytics.routes import router as expenditure_analytics_router
from app.apps.subscription_manager.routes import router as subscription_manager_router
from app.apps.scholarship_tracker.routes import router as scholarship_tracker_router
from app.apps.offline_sync.routes import router as offline_sync_router
from app.apps.auth.routes import router as auth_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(budget_router, prefix="/api/v1/budget-tracker", tags=["budget-tracker"])
app.include_router(feedback_router, prefix="/api/v1/feedback", tags=["feedback"])
app.include_router(counselling_router, prefix="/api/v1/counselling", tags=["counselling"])
app.include_router(withdrawal_router, prefix="/api/v1/withdrawal-limit", tags=["withdrawal-limit"])
app.include_router(mpesa_router, prefix="/api/v1/mpesa", tags=["mpesa"])
app.include_router(emergency_fund_router, prefix="/api/v1/emergency-fund", tags=["emergency-fund"])
app.include_router(expense_splitter_router, prefix="/api/v1/expense-splitter", tags=["expense-splitter"])
app.include_router(lending_borrowing_router, prefix="/api/v1/lending-borrowing", tags=["lending-borrowing"])
app.include_router(expenditure_analytics_router, prefix="/api/v1/expenditure-analytics", tags=["expenditure-analytics"])
app.include_router(subscription_manager_router, prefix="/api/v1/subscriptions", tags=["subscriptions"])
app.include_router(scholarship_tracker_router, prefix="/api/v1/scholarships", tags=["scholarships"])
app.include_router(offline_sync_router, prefix="/api/v1/offline", tags=["offline-sync"])

logger.info(f"{settings.PROJECT_NAME} startup complete. {len(app.routes)} routes registered.")
