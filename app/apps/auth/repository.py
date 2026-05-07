from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.apps.auth.models import User
from app.apps.auth.schemas import UserCreate
from app.core.security import get_password_hash
from typing import Optional

class AuthRepository:
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email_or_username(self, db: Session, identifier: str) -> Optional[User]:
        return db.query(User).filter(
            or_(
                User.email == identifier,
                User.username == identifier
            )
        ).first()

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
        
    def create_user(self, db: Session, data: UserCreate) -> User:
        hashed_password = get_password_hash(data.password)
        db_user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.flush()
        db.refresh(db_user)
        return db_user
