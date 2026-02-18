# File Sharing SaaS — Backend

A multi-tenant REST API for secure file sharing, built with FastAPI and PostgreSQL.

## Features

- **Multi-tenancy** — users and files are fully isolated per tenant, with per-tenant storage quotas
- **JWT auth** — access + refresh token flow, bcrypt password hashing
- **File management** — upload, download, list, soft delete with storage tracking
- **Role-based users** — `admin` / `member` roles per tenant

## Tech Stack

- FastAPI, SQLAlchemy 2, PostgreSQL, Alembic
- python-jose (JWT), passlib/bcrypt (passwords)
- pytest + httpx (tests run against SQLite in-memory)

## Project Structure

```
src/
├── main.py
└── app/
    ├── api/v1/endpoints/   # auth, users, tenants, files
    ├── core/               # config, security, deps
    ├── db/                 # session, base model
    ├── models/             # SQLAlchemy models
    ├── schemas/            # Pydantic schemas
    └── services/           # storage service
tests/
    ├── conftest.py         # SQLite test DB + fixtures
    ├── test_auth.py
    ├── test_users.py
    └── test_files.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login, get JWT tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/users/me` | Get current user |
| PUT | `/api/v1/users/me` | Update profile |
| DELETE | `/api/v1/users/me` | Deactivate account |
| POST | `/api/v1/tenants/` | Create a tenant |
| GET | `/api/v1/tenants/{id}` | Get tenant by ID |
| POST | `/api/v1/files/upload` | Upload a file |
| GET | `/api/v1/files/` | List tenant files |
| GET | `/api/v1/files/{id}` | Get file metadata |
| GET | `/api/v1/files/{id}/download` | Download file |
| DELETE | `/api/v1/files/{id}` | Delete file |

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env with your database credentials

cd src
uvicorn main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Running Tests

```bash
pip install -r requirements.txt
pytest
```

Tests use an in-memory SQLite database — no PostgreSQL required to run them.
