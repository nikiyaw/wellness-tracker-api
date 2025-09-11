from fastapi.testclient import TestClient

def test_create_habit(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/v1/habits/",
        json={"name": "Read a book"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Read a book"
    assert "id" in response.json()
    assert "user_id" in response.json()

def test_read_habits_for_user(authenticated_client: TestClient):
    # Create a habit for the user provided by the fixture
    authenticated_client.post(
        "/v1/habits/",
        json={"name": "Meditate daily"}
    )
    # Get all habits for this user
    response = authenticated_client.get("/v1/habits/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Meditate daily"

def test_read_single_habit(authenticated_client: TestClient):
    # Create a habit and get its ID
    create_response = authenticated_client.post(
        "/v1/habits/",
        json={"name": "Workout"}
    )
    habit_id = create_response.json()["id"]

    # Get the habit by its ID
    response = authenticated_client.get(f"/v1/habits/{habit_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Workout"

def test_read_nonexistent_habit(authenticated_client: TestClient):
    response = authenticated_client.get("/v1/habits/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"

def test_update_habit(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/v1/habits/",
        json={"name": "Old name"}
    )
    habit_id = create_response.json()["id"]

    response = authenticated_client.put(
        f"/v1/habits/{habit_id}",
        json={"name": "New name"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New name"

def test_delete_habit(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/v1/habits/",
        json={"name": "Habit to delete"}
    )
    habit_id = create_response.json()["id"]

    # Delete the habit
    response = authenticated_client.delete(f"/v1/habits/{habit_id}")
    assert response.status_code == 204
    
    # Try to retrieve it to confirm deletion
    check_response = authenticated_client.get(f"/v1/habits/{habit_id}")
    assert check_response.status_code == 404