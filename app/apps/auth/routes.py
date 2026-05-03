from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.settings import settings
from app.apps.auth.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.apps.auth.service import AuthService
from app.apps.auth.providers import get_auth_service, get_current_user
from app.apps.auth.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    data: UserCreate, 
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service)
):
    return service.register_user(db, data)

@router.post("/login", response_model=TokenResponse)
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service)
):
    user = service.authenticate_user(db, data)
    access_token = service.create_access_token(user.id)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
