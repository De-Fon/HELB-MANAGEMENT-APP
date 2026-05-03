"""
test_auth.py - Tests for the /api/v1/auth endpoints.

Covers:
- POST /register: success, duplicate email, duplicate username
- POST /login: success, wrong password, nonexistent user
- GET /me: success with token, blocked without token
"""
import pytest


class TestRegister:
    def test_register_success(self, client):
        """A new user can register with valid data."""
        response = client.post("/api/v1/auth/register", json={
            "email": "newuser@helb.com",
            "username": "newuser",
            "password": "StrongPass123!"
        })
        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "newuser@helb.com"
        assert body["username"] == "newuser"
        assert body["is_active"] is True
        # Password must never be returned in the response
        assert "password" not in body
        assert "hashed_password" not in body

    def test_register_duplicate_email(self, client, registered_user):
        """Registering with an already-taken email returns 400."""
        response = client.post("/api/v1/auth/register", json={
            "email": "testuser@helb.com",   # same email as registered_user fixture
            "username": "different_username",
            "password": "AnotherPass123!"
        })
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self, client, registered_user):
        """Registering with an already-taken username returns 400."""
        response = client.post("/api/v1/auth/register", json={
            "email": "different@helb.com",
            "username": "testuser",         # same username as registered_user fixture
            "password": "AnotherPass123!"
        })
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_invalid_email_format(self, client):
        """Schema validation rejects a malformed email."""
        response = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "username": "someuser",
            "password": "Pass123!"
        })
        assert response.status_code == 422


class TestLogin:
    def test_login_success_with_email(self, client, registered_user):
        """A registered user can log in using their email."""
        response = client.post("/api/v1/auth/login", json={
            "email_or_username": "testuser@helb.com",
            "password": "SecurePass123!"
        })
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert body["expires_in"] > 0

    def test_login_success_with_username(self, client, registered_user):
        """A registered user can log in using their username."""
        response = client.post("/api/v1/auth/login", json={
            "email_or_username": "testuser",
            "password": "SecurePass123!"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client, registered_user):
        """Logging in with a wrong password returns 401."""
        response = client.post("/api/v1/auth/login", json={
            "email_or_username": "testuser@helb.com",
            "password": "WrongPassword!"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Logging in with a non-existent identifier returns 401."""
        response = client.post("/api/v1/auth/login", json={
            "email_or_username": "ghost@nowhere.com",
            "password": "SomePass123!"
        })
        assert response.status_code == 401


class TestMe:
    def test_get_me_success(self, client, auth_headers, registered_user):
        """Authenticated user can fetch their own profile."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["email"] == registered_user["email"]
        assert body["username"] == registered_user["username"]

    def test_get_me_no_token(self, client):
        """Accessing /me without a token is blocked with 401."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client):
        """Accessing /me with a forged token returns 401."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer this.is.fake"}
        )
        assert response.status_code == 401
