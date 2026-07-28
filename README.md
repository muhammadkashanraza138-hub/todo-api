# Todo API using FastAPI

## Project Description

This is a simple CRUD (Create, Read, Update, Delete) REST API built using FastAPI. It allows users to manage a list of tasks through different HTTP methods.

---

## Features

- Create a new task
- Read all tasks
- Update an existing task
- Delete a task
- Interactive API documentation using Swagger UI

---

## Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

## How to Run the Project

1. Clone the repository.
2. Open the project folder.
3. Create a virtual environment.
4. Activate the virtual environment.
5. Install dependencies:

```
pip install fastapi uvicorn
```

6. Run the server:

```
uvicorn main:app --reload
```

7. Open:

```
http://127.0.0.1:8000/docs
```

to test the API.

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Welcome Message |
| GET | /tasks | Get All Tasks |
| POST | /tasks | Add New Task |
| PUT | /tasks/{task_id} | Update Task |
| DELETE | /tasks/{task_id} | Delete Task |

---

## Author

Muhammad Kashan Raza