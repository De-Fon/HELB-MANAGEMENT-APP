from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.settings import settings
from app.core.rate_limiting import limiter
from app.apps.auth.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.apps.auth.service import AuthService
from app.apps.auth.providers import get_auth_service, get_current_user
from app.apps.auth.models import User
from app.apps.idempotency.dependencies import idempotent
from app.apps.idempotency.providers import get_idempotency_service
from app.apps.idempotency.service import IdempotencyService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
@idempotent()
@limiter.limit("3/5minutes")  # 3 requests per 5 minutes
def register(
    request: Request,
    response: Response,
    data: UserCreate, 
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    return service.register_user(db, data)

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/5minutes")  # 10 requests per 5 minutes
def login(
    request: Request,
    response: Response,
    data: UserLogin,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    user = service.authenticate_user(db, data)
    access_token = service.create_access_token(user.id)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me", response_model=UserResponse)
@limiter.limit("30/minute")  # 30 requests per minute
def get_me(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service)
):
    return current_user
