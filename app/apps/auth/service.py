from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.auth.repository import AuthRepository
from app.apps.auth.schemas import UserCreate, UserLogin
from app.apps.auth.models import User
from app.core.security import verify_password, create_access_token as generate_jwt
from app.core.settings import settings

class AuthService:
    def __init__(
        self, 
        repository: AuthRepository,
        idempotency_service=None,
        rate_limit_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
        self.rate_limit_service = rate_limit_service

    def register_user(self, db: Session, data: UserCreate) -> User:
        """
        Registers a new user. 
        Uses a robust 'Try-Create' pattern to handle potential race conditions
        on unique constraints (email/username).
        """
        try:
            user = self.repository.create_user(db, data)
            db.commit()
            return user
        except Exception as e:
            db.rollback()
            # Check if it's a unique constraint violation
            error_msg = str(e).lower()
            if "email" in error_msg:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            if "username" in error_msg:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
            
            # Generic error for other integrity issues
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Could not complete registration. Please try again."
            )

    def authenticate_user(self, db: Session, data: UserLogin) -> User:
        user = self.repository.get_user_by_email_or_username(db, data.email_or_username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_access_token(self, user_id: int, expires_delta_minutes: int = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        return generate_jwt(data={"sub": str(user_id)})
