from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.apps.auth.repository import AuthRepository
from app.apps.auth.schemas import UserCreate, UserLogin
from app.apps.auth.models import User
from app.core.security import verify_password, create_access_token as generate_jwt
from app.core.config import settings
from app.apps.auth.tasks import send_welcome_email_task

class AuthService:
    def __init__(
        self, 
        repository: AuthRepository,
        idempotency_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
    def register_user(self, db: Session, data: UserCreate) -> User:
        """
        Registers a new user. 
        Uses a robust 'Try-Create' pattern to handle potential race conditions
        on unique constraints (email/username).
        """
        if self.repository.get_user_by_email(db, data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if self.repository.get_user_by_username(db, data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        try:
            user = self.repository.create_user(db, data)
            db.commit()
            
            # Trigger background welcome email
            send_welcome_email_task.delay(user.email, user.username)
            
            return user
        except IntegrityError as e:
            db.rollback()
            constraint_name = getattr(getattr(e, "orig", None), "diag", None)
            constraint_name = getattr(constraint_name, "constraint_name", "") or ""
            error_msg = f"{constraint_name} {e.orig}".lower()

            if "username" in error_msg:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
            if "email" in error_msg:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Could not complete registration. Please try again."
            )
        except Exception:
            db.rollback()
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
