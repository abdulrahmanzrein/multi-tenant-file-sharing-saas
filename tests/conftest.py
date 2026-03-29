import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.core.deps import get_db
from app.models.tenant import Tenant
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client(tmp_path):
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    from app.core import config
    original_upload_dir = config.settings.UPLOAD_DIR
    config.settings.UPLOAD_DIR = tmp_path

    app.state.limiter.enabled = False
    with TestClient(app) as c:
        yield c
    app.state.limiter.enabled = True

    config.settings.UPLOAD_DIR = original_upload_dir
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def tenant(client):
    # Create tenant directly in DB — bypasses API auth, which is correct for test setup
    db = TestingSessionLocal()
    try:
        t = Tenant(name="Test Co", slug="test-co")
        db.add(t)
        db.commit()
        db.refresh(t)
        return {"id": str(t.id), "name": t.name, "slug": t.slug}
    finally:
        db.close()


@pytest.fixture
def registered_user(client, tenant):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
        "tenant_id": tenant["id"],
    })
    return {"email": "test@example.com", "password": "password123"}


@pytest.fixture
def auth_headers(client, registered_user):
    res = client.post("/api/v1/auth/login", json=registered_user)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_user(client, tenant):
    from app.core.security import hash_password
    from app.models.user import User
    db = TestingSessionLocal()
    try:
        u = User(
            email="admin@example.com",
            hashed_password=hash_password("adminpass"),
            full_name="Admin User",
            role="admin",
            tenant_id=uuid.UUID(tenant["id"]),
        )
        db.add(u)
        db.commit()
    finally:
        db.close()
    return {"email": "admin@example.com", "password": "adminpass"}


@pytest.fixture
def admin_headers(client, admin_user):
    res = client.post("/api/v1/auth/login", json=admin_user)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

