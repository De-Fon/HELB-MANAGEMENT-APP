from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.settings import settings
from app.apps.auth.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.apps.auth.service import AuthService
from app.apps.auth.providers import get_auth_service, get_current_user
from app.apps.auth.models import User
from app.apps.idempotency.dependencies import idempotent
from app.apps.rate_limiting.dependencies import rate_limit
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.rate_limiting.providers import get_rate_limit_service
from app.apps.idempotency.service import IdempotencyService
from app.apps.rate_limiting.service import RateLimitService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
@idempotent()
@rate_limit(max_requests=3, window_seconds=300)
def register(
    request: Request,
    data: UserCreate, 
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
    # Required for decorators to find them if not already in signature
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service) 
):
    return service.register_user(db, data)

@router.post("/login", response_model=TokenResponse)
@rate_limit(max_requests=10, window_seconds=300)
def login(
    request: Request,
    data: UserLogin,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    user = service.authenticate_user(db, data)
    access_token = service.create_access_token(user.id)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me", response_model=UserResponse)
@rate_limit(max_requests=30, window_seconds=60)
def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    rate_limit_service: RateLimitService = Depends(get_rate_limit_service)
):
    return current_user
