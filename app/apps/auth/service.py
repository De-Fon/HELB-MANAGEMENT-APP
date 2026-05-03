from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.auth.repository import AuthRepository
from app.apps.auth.schemas import UserCreate, UserLogin
from app.apps.auth.models import User
from app.core.security import verify_password, create_access_token as generate_jwt
from app.core.settings import settings

class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register_user(self, db: Session, data: UserCreate) -> User:
        existing_user = self.repository.get_user_by_email_or_username(db, data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            
        existing_username = self.repository.get_user_by_email_or_username(db, data.username)
        if existing_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
            
        user = self.repository.create_user(db, data)
        db.commit()
        return user

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
