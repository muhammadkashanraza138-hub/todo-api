from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
import psycopg2
import os


load_dotenv()

app = FastAPI(
    title="Todo API with Supabase Authentication"
)


# -----------------------------
# PostgreSQL Database Connection
# -----------------------------

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()


# -----------------------------
# Supabase Connection
# -----------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------
# Security
# -----------------------------

security = HTTPBearer()


# -----------------------------
# Models
# -----------------------------

class Task(BaseModel):
    task: str


class User(BaseModel):
    email: str
    password: str


# -----------------------------
# Reusable Protected Route Dependency
# -----------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        result = supabase.auth.get_user(token)

        if result.user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return result.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# -----------------------------
# Home Page
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to my Todo API!"
    }


# -----------------------------
# Public Route
# -----------------------------

@app.get("/public/info")
def public_info():
    return {
        "message": "This is public information. No login is required."
    }


# -----------------------------
# Signup
# -----------------------------

@app.post("/auth/signup", status_code=201)
def signup(user: User):

    if user.email.strip() == "" or user.password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        result = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        return {
            "message": "Signup successful",
            "user": result.user
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Signup failed. Email may already be registered."
        )


# -----------------------------
# Login
# -----------------------------

@app.post("/auth/login")
def login(user: User):

    if user.email.strip() == "" or user.password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        result = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        return {
            "message": "Login successful",
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )


# -----------------------------
# Logout
# -----------------------------

@app.post("/auth/logout", status_code=204)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        supabase.auth.get_user(token)
        return Response(status_code=204)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# -----------------------------
# Protected Profile Route
# -----------------------------

@app.get("/protected/profile")
def protected_profile(user=Depends(get_current_user)):

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


# -----------------------------
# Protected Dashboard Route
# -----------------------------

@app.get("/protected/dashboard")
def protected_dashboard(user=Depends(get_current_user)):

    return {
        "message": "Welcome to your protected dashboard!",
        "user_id": user.id,
        "email": user.email
    }


# -----------------------------
# Read All Tasks
# -----------------------------

@app.get("/tasks")
def get_tasks():

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return {
        "tasks": tasks
    }


# -----------------------------
# Add New Task
# -----------------------------

@app.post("/tasks")
def add_task(task: Task):

    if task.task.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Task cannot be empty"
        )

    cursor.execute(
        "INSERT INTO tasks (task) VALUES (%s) RETURNING id",
        (task.task,)
    )

    task_id = cursor.fetchone()[0]
    conn.commit()

    return {
        "message": "Task added successfully",
        "id": task_id,
        "task": task.task
    }


# -----------------------------
# Update Task
# -----------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    cursor.execute(
        "UPDATE tasks SET task = %s WHERE id = %s",
        (task.task, task_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task updated successfully"
    }


# -----------------------------
# Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }