import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db

# Use an in-memory SQLite database for test isolation.
# This ensures tests are fast and don't interfere with your dev database.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    """
    This fixture ensures a clean database for each test function.
    It creates all tables before a test runs and drops them after.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """
    Provides a TestClient for making API requests.
    It overrides the dependency to use the test database.
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_client(client: TestClient):
    """
    Provides a TestClient that is already logged in with a valid JWT.
    This prevents code duplication in tests that require authentication.
    """
    # Create a user for the test
    client.post(
        "/v1/users/",
        json={"email": "testuser@example.com", "password": "testpassword"}
    )
    # Login to get a token
    login_response = client.post(
        "/v1/users/token",
        data={"username": "testuser@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    # Add the token to the client's headers
    client.headers = {"Authorization": f"Bearer {token}"}
    return client