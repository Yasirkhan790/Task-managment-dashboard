"""Tests for account and task endpoints."""
def register_and_login(client):
    registration = client.post("/api/auth/register", json={"email": "student@example.com", "full_name": "Python Student", "password": "strong-pass-123"})
    assert registration.status_code == 201
    login = client.post("/api/auth/login", data={"username": "student@example.com", "password": "strong-pass-123"})
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_duplicate_email(client):
    payload = {"email": "duplicate@example.com", "full_name": "Test User", "password": "strong-pass-123"}
    assert client.post("/api/auth/register", json=payload).status_code == 201
    assert client.post("/api/auth/register", json=payload).status_code == 409

def test_task_crud_flow(client):
    headers = register_and_login(client)
    created = client.post("/api/tasks", headers=headers, json={"title": "Learn FastAPI", "description": "Build a REST API"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert created.json()["status"] == "todo"
    listed = client.get("/api/tasks", headers=headers)
    assert listed.status_code == 200 and len(listed.json()) == 1
    updated = client.patch(f"/api/tasks/{task_id}", headers=headers, json={"status": "done"})
    assert updated.status_code == 200 and updated.json()["status"] == "done"
    deleted = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/tasks/{task_id}", headers=headers).status_code == 404

def test_tasks_require_authentication(client):
    assert client.get("/api/tasks").status_code == 401
