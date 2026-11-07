# Task Management API

A beginner-to-intermediate Python backend project. It provides user registration, JWT login, and task management through a REST API.

## Features
- Register accounts and securely hash passwords with Argon2.
- Log in and receive signed JWT access tokens.
- Read the current user's profile.
- Create, list, view, update, and delete tasks.
- Keep each user's tasks private.
- Filter tasks by status or title and paginate results.
- Explore interactive API documentation.
- Run automated tests with an isolated in-memory SQLite database.

## Technology
- Python: application language.
- FastAPI: HTTP API framework and OpenAPI documentation.
- SQLAlchemy: database models, relationships, and queries.
- SQLite: local relational database.
- Pydantic: request validation and response serialization.
- pwdlib + Argon2: password hashing.
- python-jose: JWT creation and validation.
- Pytest + HTTPX: automated API tests.

## Windows PowerShell setup
```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
# If activation is blocked:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
py -m uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Swagger docs: http://127.0.0.1:8000/docs  
ReDoc: http://127.0.0.1:8000/redoc  
Health check: http://127.0.0.1:8000/health

## Authentication workflow
1. POST /api/auth/register with email, full_name, and password.
2. POST /api/auth/login as form data. Use the email in username and password in password.
3. Copy access_token from the response.
4. Click Authorize in Swagger and enter the token.
5. Call protected task endpoints.

## API endpoints
| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | / | Welcome | No |
| GET | /health | Health check | No |
| POST | /api/auth/register | Register | No |
| POST | /api/auth/login | Login | No |
| GET | /api/auth/me | Current profile | Yes |
| POST | /api/tasks | Create task | Yes |
| GET | /api/tasks | List tasks | Yes |
| GET | /api/tasks/{task_id} | Get task | Yes |
| PATCH | /api/tasks/{task_id} | Update task | Yes |
| DELETE | /api/tasks/{task_id} | Delete task | Yes |

Task status values: todo, in_progress, done.  
List query parameters: status, search, skip, limit (maximum 100).

## Run tests
```powershell
py -m pytest -v
```

## Structure
```text
backend/
├── app/
│   ├── routers/auth.py
│   ├── routers/tasks.py
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
└── requirements.txt
```

## Production improvements
This is a learning project. Before production, add Alembic migrations, rate limiting, refresh-token rotation, stricter CORS policy, structured logging, HTTPS deployment, and secret management. Change SECRET_KEY before deployment.
