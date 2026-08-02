from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI(
    title="Todo API with Authentication",
    description="FastAPI Todo API using PostgreSQL and Supabase Authentication",
    version="1.0.0"
)
security = HTTPBearer()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

# Connect to Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create the tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
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
        "INSERT INTO tasks (title, done) VALUES (%s, %s)",
        example_tasks
    )
    conn.commit()


# Model for a Task
class Task(BaseModel):
    title: str


# Model for User
class User(BaseModel):
    email: str
    password: str

def verify_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        result = supabase.auth.get_user(token)
        return result.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# Home Page
@app.get("/")
def home():
    return {
        "message": "Server running and connected to Supabase"
    }


# ---------------- AUTH ROUTES ---------------- #

# Signup
@app.post("/auth/signup", status_code=201)
def signup(user: User):

    if user.email.strip() == "" or user.password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Email and Password are required"
        )

    result = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password
    })

    return result


# Login
@app.post("/auth/login")
def login(user: User):

    if user.email.strip() == "" or user.password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Email and Password are required"
        )

    try:
        result = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        if result.session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid login credentials"
            )

        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

# Public Route
@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


# ---------------- TODO ROUTES ---------------- #

# Read All Tasks
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks ORDER BY id")
    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": row[2]
        })

    return tasks


# Read One Task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


# Create a New Task
@app.post("/tasks", status_code=201)
def add_task(new_task: Task):

    if new_task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s)",
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

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = %s WHERE id = %s",
        (updated_task.title, task_id)
    )

    conn.commit()

    return {
        "message": "Task updated successfully!"
    }


# Delete a Task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    return {
        "message": "Task deleted successfully!"
    }


@app.get(
    "/protected/profile",
    dependencies=[Depends(security)]
)
def protected_profile(user=Depends(verify_user)):

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }
@app.get(
    "/protected/dashboard",
    dependencies=[Depends(security)]
)
def dashboard(user=Depends(verify_user)):

    return {
        "message": "Welcome to your dashboard!",
        "email": user.email
    }

@app.post(
    "/auth/logout",
    status_code=204,
    dependencies=[Depends(security)]
)
def logout(user=Depends(verify_user)):

    try:
        supabase.auth.sign_out()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Logout failed"
        )

    return