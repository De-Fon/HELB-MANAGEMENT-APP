from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.settings import settings

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# SessionLocal class for creating new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency for FastAPI to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
