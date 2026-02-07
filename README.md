# File Sharing SaaS Backend

This project is a multi-tenant SaaS backend for secure, permissioned file sharing.

## Goal
Learn and demonstrate real-world backend architecture:
- multi-tenancy
- role-based access control
- file collaboration

## Status
Initial setup - skeleton structure created.

## Project Structure

```
src/
├── main.py                    # FastAPI entry point
└── app/
    ├── api/v1/               # API version 1
    │   ├── router.py         # Main API router
    │   └── endpoints/        # Route handlers
    │       ├── auth.py       # Authentication endpoints
    │       ├── users.py      # User management
    │       ├── tenants.py    # Tenant management
    │       └── files.py      # File operations
    ├── core/                 # Core functionality (config, security, deps)
    ├── db/                   # Database (session, base)
    ├── models/               # SQLAlchemy models
    ├── schemas/              # Pydantic schemas
    ├── services/             # Business logic
    ├── middleware/           # Custom middleware
    └── utils/                # Helper functions
```

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run the server:**
   ```bash
   cd src
   uvicorn main:app --reload
   ```

5. **View API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Next Steps

- Implement database models in `app/models/`
- Create Pydantic schemas in `app/schemas/`
- Set up database connection in `app/db/`
- Add JWT authentication in `app/core/security.py`
- Implement endpoint logic in `app/api/v1/endpoints/`
