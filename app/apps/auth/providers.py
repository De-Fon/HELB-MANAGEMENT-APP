from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.database import get_db
from app.core.settings import settings
from app.apps.auth.repository import AuthRepository
from app.apps.auth.service import AuthService
from app.apps.auth.models import User
from app.apps.request_control.providers import get_idempotency_service, get_rate_limit_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_auth_repository() -> AuthRepository:
    return AuthRepository()

def get_auth_service(
    repository: AuthRepository = Depends(get_auth_repository),
    idempotency_service = Depends(get_idempotency_service, use_cache=True),
    rate_limit_service = Depends(get_rate_limit_service, use_cache=True)
) -> AuthService:
    return AuthService(
        repository=repository,
        idempotency_service=idempotency_service,
        rate_limit_service=rate_limit_service
    )

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db),
    repo: AuthRepository = Depends(get_auth_repository)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
        
    user = repo.get_user_by_id(db, user_id)
    
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
