# Task Management API

A Python REST API for managing personal tasks. This project is built with FastAPI, SQLAlchemy, SQLite, Pydantic, JWT authentication, and Pytest.

> The backend source code lives in the `backend/` directory.

## Features

- Register a user account with an email address and password.
- Hash passwords with Argon2 before saving them.
- Log in and receive a signed JWT access token.
- View the authenticated user's profile.
- Create, read, update, and delete tasks.
- Keep each user's tasks private.
- Filter tasks by status and search task titles.
- Paginate task results.
- Explore endpoints through interactive Swagger documentation.
- Run automated API tests.

## Technology stack

| Technology | What it does |
| --- | --- |
| Python | Main programming language |
| FastAPI | Builds HTTP endpoints and API documentation |
| SQLAlchemy | Maps Python classes to database tables and runs queries |
| SQLite | Stores users and tasks in a local database file |
| Pydantic | Validates request data and formats responses |
| JWT | Provides signed access tokens for authentication |
| pwdlib / Argon2 | Securely hashes passwords |
| Pytest | Runs automated tests |
| HTTPX | Sends HTTP requests during API tests |
| Uvicorn | Runs the FastAPI application server |

## Project structure

```text
backend/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run locally on Windows

Open PowerShell and run:

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Install dependencies and create your local environment file:

```powershell
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Start the API:

```powershell
py -m uvicorn app.main:app --reload
```

Open these URLs:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API endpoints

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| GET | `/` | API welcome message | No |
| GET | `/health` | Health check | No |
| POST | `/api/auth/register` | Register a user | No |
| POST | `/api/auth/login` | Log in and receive a token | No |
| GET | `/api/auth/me` | Get current user profile | Yes |
| POST | `/api/tasks` | Create a task | Yes |
| GET | `/api/tasks` | List your tasks | Yes |
| GET | `/api/tasks/{task_id}` | Get one of your tasks | Yes |
| PATCH | `/api/tasks/{task_id}` | Update one of your tasks | Yes |
| DELETE | `/api/tasks/{task_id}` | Delete one of your tasks | Yes |

Task status values are `todo`, `in_progress`, and `done`.

The task list supports `status`, `search`, `skip`, and `limit` query parameters.

## Authentication workflow

1. Send a POST request to `/api/auth/register` with `email`, `full_name`, and `password`.
2. Send a POST request to `/api/auth/login` using form fields `username` (your email) and `password`.
3. Copy the `access_token` from the response.
4. In Swagger UI, click **Authorize** and enter the token.
5. Use the protected task endpoints.

## Run automated tests

From the `backend/` directory, with the virtual environment activated:

```powershell
py -m pytest -v
```

Tests use a temporary in-memory SQLite database, so they do not modify your local application database.

## Detailed backend documentation

See [backend/README.md](backend/README.md) for backend setup, endpoint details, and additional implementation notes.

## Security and production notes

This repository is a learning project. Before a production deployment:

- Set a strong, private `SECRET_KEY` in your environment.
- Never commit your real `.env` file or database credentials.
- Configure HTTPS and restrictive CORS settings.
- Add database migrations, rate limiting, refresh-token rotation, and production logging.
- Review authentication, authorization, and deployment settings.

Do not use the example development secret in a public deployment.
