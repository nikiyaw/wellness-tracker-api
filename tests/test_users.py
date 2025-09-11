from fastapi.testclient import TestClient

# The fixtures from conftest.py are automatically available here.

def test_create_user(client: TestClient):
    response = client.post(
        "/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "created_at" in response.json()

def test_create_user_duplicate_email(client: TestClient):
    # Create the user once
    client.post(
        "/v1/users/",
        json={"email": "duplicate@example.com", "password": "password"}
    )
    # Try to create the same user again
    response = client.post(
        "/v1/users/",
        json={"email": "duplicate@example.com", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_for_access_token(client: TestClient):
    # Create a user first
    client.post(
        "/v1/users/",
        json={"email": "login_test@example.com", "password": "testpassword"}
    )
    # Now, test the token endpoint
    login_response = client.post(
        "/v1/users/token",
        data={"username": "login_test@example.com", "password": "testpassword"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"