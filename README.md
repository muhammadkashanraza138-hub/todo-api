# Todo API with PostgreSQL

## Project Description

This project is a CRUD (Create, Read, Update, Delete) Todo API built using FastAPI and PostgreSQL running inside Docker.

## Technologies Used

- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Python

## How to Run

Clone the repository:

```bash
git clone https://github.com/muhammadkashanraza138-hub/todo-api.git
```

Go to the project folder:

```bash
cd todo-api
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Environment Variables

Create a `.env` file using `.env.example`.

## Database

PostgreSQL runs inside Docker.

## Persistence

Data was tested by:

1. Creating tasks.
2. Running:

```bash
docker compose down
docker compose up -d
```

3. Restarting FastAPI.
4. Verifying that all tasks were still present.

This confirms the database persists using a Docker volume.