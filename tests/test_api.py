from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_create_task_rejects_spaces_only_title():
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 400
    assert response.json() == {"detail": "Title cannot be empty"}

def test_create_and_get_task(clean_database):
    response = client.post(
        "/tasks",
        json={"title": "  Integration test task  "},
    )
    assert response.status_code == 201

    created = response.json()
    assert created["title"] == "Integration test task"
    assert created["completed"] is False

    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created

def test_complete_task(clean_database):
    response = client.post("/tasks", json={"title": "Complete this task"})
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_delete_task(clean_database):
    response = client.post("/tasks", json={"title": "Delete this task"})
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_list_tasks(clean_database):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/tasks", json={"title": "Test task listing"})
    assert response.status_code == 201
    created = response.json()

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [created]

def test_missing_title_returns_422():
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_missing_task_returns_404(clean_database):
    responses = [
        client.get("/tasks/999"),
        client.patch("/tasks/999/complete"),
        client.delete("/tasks/999"),
    ]

    for response in responses:
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}