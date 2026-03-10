# File Sharing SaaS — Backend

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)
![Tests](https://img.shields.io/badge/tests-27%20passing-brightgreen?style=flat-square)

A production-ready REST API for multi-tenant file sharing. Each organization gets an isolated workspace with its own users, files, and enforced storage quota. Built to demonstrate real-world SaaS backend patterns: tenant isolation, JWT auth flows, audit logging, storage abstraction, and rate limiting.

---

## Features

- **Multi-tenancy** — complete data isolation per tenant enforced at the query layer; users can only access their own tenant's resources
- **JWT auth** — access + refresh token flow with token type validation; bcrypt password hashing
- **File management** — upload, download, list (paginated), soft delete; storage usage tracked atomically per tenant
- **Storage quota enforcement** — quota check happens after the file is written to get the real size, with automatic cleanup on overflow
- **Shareable links** — generate public download tokens with optional expiry; expired links return `410 Gone`
- **Audit logging** — every file upload, download, and delete is logged in the same DB transaction as the action
- **Rate limiting** — 5 req/min on login (brute force protection), 20 req/min on upload (abuse prevention)
- **Role-based access** — `admin` / `member` roles per tenant with enforced route guards
- **Docker support** — single `docker compose up` spins up the app + PostgreSQL
- **Seed script** — creates sample tenants and users for local development

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI 0.115 |
| ORM | SQLAlchemy 2 |
| Database | PostgreSQL 15 |
| Migrations | Alembic |
| Auth | python-jose (JWT), passlib/bcrypt |
| Rate limiting | slowapi |
| Testing | pytest, httpx (SQLite in-memory) |
| Containers | Docker, docker-compose |

---

## Project Structure

```
src/
└── app/
    ├── api/v1/endpoints/   # auth, users, tenants, files, shares
    ├── core/               # config, security, deps, limiter
    ├── db/                 # session, base model
    ├── models/             # SQLAlchemy models (User, File, Tenant, AuditLog, SharedLink)
    ├── schemas/            # Pydantic request/response schemas
    └── services/           # file_service, share_service, audit_service, storage
tests/
    ├── conftest.py         # SQLite in-memory DB + shared fixtures
    ├── test_auth.py
    ├── test_users.py
    ├── test_files.py
    ├── test_tenants.py
    └── test_shares.py
scripts/
    └── seed.py             # Creates sample tenants and users
```

---

## API Reference

### Auth
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | — | Register a new user under a tenant |
| POST | `/api/v1/auth/login` | — | Login, returns access + refresh tokens |
| POST | `/api/v1/auth/refresh` | — | Exchange refresh token for new token pair |

### Users
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/users/me` | Bearer | Get current user profile |
| PUT | `/api/v1/users/me` | Bearer | Update name or email |
| DELETE | `/api/v1/users/me` | Bearer | Deactivate account |

### Tenants
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/tenants/` | Bearer (admin) | Create a tenant |
| GET | `/api/v1/tenants/` | Bearer (admin) | List all tenants |
| GET | `/api/v1/tenants/{id}` | Bearer | Get tenant by ID |

### Files
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/files/upload` | Bearer | Upload a file (20 req/min) |
| GET | `/api/v1/files/` | Bearer | List tenant files (paginated) |
| GET | `/api/v1/files/{id}` | Bearer | Get file metadata |
| GET | `/api/v1/files/{id}/download` | Bearer | Download file |
| DELETE | `/api/v1/files/{id}` | Bearer | Soft delete file |

### Sharing
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/files/{id}/share` | Bearer | Create a public share link (optional `expires_at`) |
| GET | `/api/v1/share/{token}` | — | Download file via share token |

---

## Local Setup

```bash
git clone https://github.com/abdulrahmanzrein/multi-tenant-file-sharing-saas.git
cd multi-tenant-file-sharing-saas

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Set DATABASE_URL, SECRET_KEY, UPLOAD_DIR in .env

cd src
alembic upgrade head
uvicorn main:app --reload
```

Swagger UI: `http://localhost:8000/docs`

## Docker

```bash
docker compose up --build
```

Starts the API on port `8000` and PostgreSQL on port `5432`. To seed sample data:

```bash
docker compose exec app python ../scripts/seed.py
```

## Running Tests

```bash
cd src
pytest ../tests/ -v
```

Tests run against an in-memory SQLite database — no PostgreSQL or running server required.

---

## Design Notes

**Tenant isolation** is enforced at the service layer — every query filters by `tenant_id` derived from the authenticated user's JWT. There is no middleware-level row filtering; isolation is explicit and auditable.

**Quota enforcement** saves the file first to get the actual size on disk, then checks `storage_used + size > limit`. If over quota, the file is deleted and a `413` is returned. This avoids the TOCTOU bug of checking before writing.

**Audit logging** stages the audit log entry in the same SQLAlchemy session as the action it records, so both are committed atomically. There are no phantom audit entries from failed operations.

**Storage abstraction** uses an ABC (`StorageBackend`) so the local filesystem implementation can be swapped for S3 or GCS without touching service or endpoint code.
