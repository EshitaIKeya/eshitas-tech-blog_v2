"""
Basic API tests using FastAPI TestClient + SQLite in-memory database.
Run with: pytest tests/ -v   (from inside the backend/ folder)
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import database
from app.database import Base
from app.dependencies import get_db

# Use SQLite in memory for tests (no PostgreSQL needed)
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=test_engine)

# Point the app's database module at the test engine/session BEFORE
# importing app.main, since main.py's startup event uses app.database.engine
# and seed.py uses app.database.SessionLocal directly.
database.engine = test_engine
database.SessionLocal = TestSession

from app.main import app  # noqa: E402  (must import after patching database)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


# Tell FastAPI to use the test database instead of PostgreSQL
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    """TestClient as a context manager triggers FastAPI's startup event,
    which creates tables and seeds default data against our SQLite engine."""
    with TestClient(app) as c:
        yield c


# --- TESTS ---

def test_health_check(client):
    """The root endpoint should return a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_get_posts_empty(client):
    """GET /posts/ should return a paginated post list."""
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert "page" in data


def test_register_user(client):
    """POST /auth/register should create a new user."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
    })
    assert response.status_code == 200


def test_register_duplicate_user(client):
    """Registering the same username twice should fail with 400."""
    payload = {
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "pass123",
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_wrong_password(client):
    """Login with wrong password should return 400."""
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpass",
    })
    assert response.status_code == 400


def test_protected_endpoint_without_token(client):
    """Accessing /auth/me with no token at all should return 401 (Unauthorized)."""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_create_post_without_auth(client):
    """Creating a post with no token at all should return 401 (Unauthorized)."""
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "Test content",
        "category_id": 1,
    })
    assert response.status_code == 401


def test_get_categories(client):
    """GET /categories/ should return a list (seeded with 5 defaults)."""
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_login_success_after_register(client):
    """A registered user should be able to log in and get a token."""
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "mypassword123",
    })
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "mypassword123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

