from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ===== TEST HOME ENDPOINT =====
def test_home():
    """Test home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Todo API"

# ===== TEST HEALTH ENDPOINT =====
def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ===== TEST GET TODOS (EMPTY) =====
def test_get_todos_empty():
    """Test getting todos when empty"""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json()["todos"] == []

# ===== TEST CREATE TODO =====
def test_create_todo():
    """Test creating a todo"""
    new_todo = {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    }
    response = client.post("/todos", json=new_todo)
    assert response.status_code == 200
    assert response.json()["created"]["title"] == "Learn FastAPI"

# ===== TEST GET TODO BY ID =====
def test_get_todo():
    """Test getting a single todo"""
    # First create a todo
    new_todo = {
        "id": 2,
        "title": "Test Todo",
        "completed": False
    }
    client.post("/todos", json=new_todo)
    
    # Then get it
    response = client.get("/todos/2")
    assert response.status_code == 200
    assert response.json()["todo"]["title"] == "Test Todo"

# ===== TEST UPDATE TODO =====
def test_update_todo():
    """Test updating a todo"""
    # Create a todo
    new_todo = {
        "id": 3,
        "title": "Old Title",
        "completed": False
    }
    client.post("/todos", json=new_todo)
    
    # Update it
    updated = {
        "id": 3,
        "title": "New Title",
        "completed": True
    }
    response = client.put("/todos/3", json=updated)
    assert response.status_code == 200
    assert response.json()["updated"]["title"] == "New Title"

# ===== TEST DELETE TODO =====
def test_delete_todo():
    """Test deleting a todo"""
    # Create a todo
    new_todo = {
        "id": 4,
        "title": "To Delete",
        "completed": False
    }
    client.post("/todos", json=new_todo)
    
    # Delete it
    response = client.delete("/todos/4")
    assert response.status_code == 200
    assert response.json()["deleted"] == 4

# ===== TEST 404 ERROR =====
def test_get_nonexistent_todo():
    """Test getting a todo that doesn't exist"""
    response = client.get("/todos/999")
    assert response.status_code == 404