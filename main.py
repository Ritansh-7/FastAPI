from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create the app
app = FastAPI(title="Todo API")

# Data model
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

# In-memory database (for demo)
todos = []

# ===== ENDPOINTS =====

@app.get("/")
def home():
    """Home endpoint"""
    return {"message": "Welcome to Todo API", "version": "1.0"}

@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}

@app.get("/todos")
def get_todos():
    """Get all todos"""
    return {"todos": todos}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    """Get a single todo by ID"""
    for todo in todos:
        if todo["id"] == todo_id:
            return {"todo": todo}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos")
def create_todo(todo: Todo):
    """Create a new todo"""
    todo_dict = todo.dict()
    todos.append(todo_dict)
    return {"created": todo_dict}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    """Update a todo"""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[i] = updated_todo.dict()
            return {"updated": todos[i]}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo"""
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return {"deleted": todo_id}

# Run the app (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)