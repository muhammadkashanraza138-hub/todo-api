from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Model for a Task
class Task(BaseModel):
    task: str

# Temporary storage (instead of a database)
tasks = [
    "Learn FastAPI",
    "Complete FlyRank Assignment",
    "Practice Python"
]

# Home Page
@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI application!"}

# Read All Tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Create a New Task
@app.post("/tasks")
def add_task(new_task: Task):
    tasks.append(new_task.task)
    return {
        "message": "Task added successfully!",
        "tasks": tasks
    }

# Update a Task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if task_id < 0 or task_id >= len(tasks):
        return {"error": "Task not found"}

    tasks[task_id] = updated_task.task
    return {
        "message": "Task updated successfully!",
        "tasks": tasks
    }

# Delete a Task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        return {"error": "Task not found"}

    deleted = tasks.pop(task_id)
    return {
        "message": f"'{deleted}' deleted successfully!",
        "tasks": tasks
    }