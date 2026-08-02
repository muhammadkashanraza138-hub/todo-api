# Assignment 04 - FastAPI Authentication with Supabase

## Description

This project is a FastAPI REST API that uses PostgreSQL for storing tasks and Supabase Authentication for user management. Users can sign up, log in, log out, and access protected endpoints using JWT authentication.

---

## Technologies Used

- Python 3
- FastAPI
- PostgreSQL
- Supabase
- psycopg2
- python-dotenv
- Uvicorn

---

## Installation

### Clone the repository

```bash
git clone <your-github-repository-url>
cd <repository-name>
```

### Create a virtual environment

```bash
python3 -m venv venv
```

### Activate it

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

SUPABASE_URL=
SUPABASE_KEY=
```

---

## Run the project

```bash
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Authentication |
|---------|----------|----------------|
| GET | / | No |
| POST | /auth/signup | No |
| POST | /auth/login | No |
| POST | /auth/logout | Yes |
| GET | /public/info | No |
| GET | /protected/profile | Yes |
| GET | /protected/dashboard | Yes |
| GET | /tasks | No |
| GET | /tasks/{id} | No |
| POST | /tasks | No |
| PUT | /tasks/{id} | No |
| DELETE | /tasks/{id} | No |

---

## Authentication

This project uses Supabase Authentication.

After logging in, an Access Token (JWT) is returned.

Use the token inside the Authorization header.

```
Bearer <your_access_token>
```

Swagger's **Authorize** button can also be used for authenticated requests.

---

## Screenshot

Add your Swagger UI screenshot here.

Example:

```
docs/swagger.png
```

---

## Author

Muhammad Kashan Raza