"""
conftest.py - Central test configuration.

Strategy:
- Uses a separate PostgreSQL test database so tests NEVER touch production data.
- Overrides the `get_db` FastAPI dependency so all routes use the test session.
- Provides reusable fixtures for: test client, registered user, and auth token.
"""
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("RATE_LIMIT_ENABLED", "false")

from app.main import app
from app.core.database import Base, get_db

# Use a dedicated PostgreSQL test database to support PG-specific types like ARRAY
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_test_db"

@pytest.fixture(scope="session")
def test_engine():
    """Create a shared PostgreSQL engine for the whole test session."""
    engine = create_engine(TEST_DATABASE_URL)
    # Create all tables from our SQLAlchemy models
    Base.metadata.create_all(bind=engine)
    yield engine
    # Tear down tables after session
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    """
    Provides a fresh, isolated DB session per test.
    Rolls back all changes after each test to keep tests independent.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides a FastAPI TestClient with the `get_db` dependency overridden
    so all HTTP requests use the isolated test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def registered_user(client):
    """Registers a fresh test user and returns the response body."""
    payload = {
        "email": "testuser@helb.com",
        "username": "testuser",
        "password": "SecurePass123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201, response.text
    return response.json()

@pytest.fixture(scope="function")
def auth_token(client, registered_user):
    """Logs in the test user and returns a valid Bearer token string."""
    payload = {
        "email_or_username": "testuser@helb.com",
        "password": "SecurePass123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def auth_headers(auth_token):
    """Returns Authorization headers dict for protected endpoint tests."""
    return {"Authorization": f"Bearer {auth_token}"}
