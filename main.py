from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")
conn.commit()

# Insert example tasks only if the table is empty
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    example_tasks = [
        ("Learn FastAPI", False),
        ("Complete FlyRank Assignment", False),
        ("Practice Python", False)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        example_tasks
    )
    conn.commit()


# Model for a Task
class Task(BaseModel):
    title: str


# Home Page
@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI application!"}


# Read All Tasks
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })

    return tasks


# Read One Task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


# Create a New Task
@app.post("/tasks", status_code=201)
def add_task(new_task: Task):

    if new_task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (new_task.title, False)
    )

    conn.commit()

    return {
        "message": "Task added successfully!"
    }


# Update a Task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):

    if updated_task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = ? WHERE id = ?",
        (updated_task.title, task_id)
    )

    conn.commit()

    return {
        "message": "Task updated successfully!"
    }


# Delete a Task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    return {
        "message": "Task deleted successfully!"
    }