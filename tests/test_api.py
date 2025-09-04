import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database.database import Base, get_db

# Use a separate, in-memory SQLite database for testing to avoid interfering with the development database. 
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the `get_db` dependency to use the test database.
def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()

# Use a fixture to manage the database and client setup for each test.
@pytest.fixture(name="client")
def client_fixture():
    # This runs BEFORE each test function
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    # This runs AFTER each test function
    Base.metadata.drop_all(bind=engine)


# --- Tests for API Endpoints ---

def test_create_user(client: TestClient):
    response = client.post(
        "/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "created_at" in response.json()

def test_login_and_create_habit(client: TestClient):
    # First, create a user using "email"
    client.post(
        "/v1/users/",
        json={"email": "test_habit_user@example.com", "password": "testpassword"}
    )

    # Then, login to get a JWT token using "username"
    login_response = client.post(
        "/v1/users/token",
        data={"username": "test_habit_user@example.com", "password": "testpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Now, create a habit using the token
    habit_response = client.post(
        "/v1/habits/",
        json={"name": "Read a book"},
        headers=headers
    )
    assert habit_response.status_code == 201
    assert habit_response.json()["name"] == "Read a book"

def test_read_habits_for_user(client: TestClient):
    # Corrected: Create user with "email"
    client.post(
        "/v1/users/",
        json={"email": "read_user@example.com", "password": "readpassword"}
    )
    # Login with "username"
    login_response = client.post(
        "/v1/users/token",
        data={"username": "read_user@example.com", "password": "readpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a habit for this user
    client.post(
        "/v1/habits/",
        json={"name": "Meditate"},
        headers=headers
    )

    # Get all habits for this user and verify
    get_response = client.get("/v1/habits/", headers=headers)
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    # Corrected: Typo "Meditatae" -> "Meditate"
    assert get_response.json()[0]["name"] == "Meditate"


# -- More In-Depth Tests ---

def test_read_nonexistent_habit(client: TestClient):
    # Corrected: Create user with "email"
    client.post(
        "/v1/users/",
        json={"email": "read_user@example.com", "password": "readpassword"}
    )
    # Login with "username"
    login_response = client.post(
        "/v1/users/token", 
        data={"username": "read_user@example.com", "password": "readpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # We are testing for a habit that does not exist (ID 999).
    response = client.get("/v1/habits/999", headers=headers)

    # We expect a 404 Not Found error.
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"

def test_update_habit(client: TestClient):
    # Corrected: Create user with "email"
    client.post(
        "/v1/users/",
        json={"email": "read_user@example.com", "password": "readpassword"}
    )
    # Login with "username"
    login_response = client.post(
        "/v1/users/token",
        data={"username": "read_user@example.com", "password": "readpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # First, create a habit to be updated. 
    create_response = client.post(
        "/v1/habits/",
        json={"name": "Old Habit Name"},
        headers=headers
    )
    habit_id = create_response.json()["id"]

    # Then, send a PUT request to update it. 
    update_response = client.put(
        f"/v1/habits/{habit_id}",
        json={"name": "New Habit Name"},
        headers=headers
    )

    # We check the response status code and the returned data. 
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Habit Name"
    assert update_response.json()["id"] == habit_id

def test_delete_habit(client: TestClient):
    # Corrected: Create user with "email"
    client.post(
        "/v1/users/",
        json={"email": "read_user@example.com", "password": "readpassword"}
    )
    # Login with "username"
    login_response = client.post(
        "/v1/users/token",
        data={"username": "read_user@example.com", "password": "readpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a habit to be deleted. 
    create_response = client.post(
        "/v1/habits/", 
        json={"name": "Habit to Delete"},
        headers=headers
    )
    habit_id = create_response.json()["id"]

    # Send a DELETE request. 
    delete_response = client.delete(
        f"/v1/habits/{habit_id}", # Corrected: use an f-string to pass the habit_id
        headers=headers
    )

    # A successful delete should return a 204 No Content status.
    assert delete_response.status_code == 204

    # Now, try to get the habit again to make sure it was deleted.
    check_response = client.get(
        f"/v1/habits/{habit_id}", 
        headers=headers
    )
    assert check_response.status_code == 404