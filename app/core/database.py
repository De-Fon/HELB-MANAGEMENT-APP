from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from app.core.settings import settings

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# --- Log database connection events via SQLAlchemy events ---
@event.listens_for(engine, "connect")
def on_connect(dbapi_connection, connection_record):
    logger.debug("Database connection established.")

@event.listens_for(engine, "handle_error")
def on_handle_error(exception_context):
    """Logs database errors captured by the engine."""
    logger.error(f"Database error captured by Engine: {exception_context.original_exception}")

# SessionLocal class for creating new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency for FastAPI to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as exc:
        # Log database errors before re-raising so they appear in errors.log
        logger.error(f"Database error during request: {exc}")
        raise
    finally:
        db.close()
