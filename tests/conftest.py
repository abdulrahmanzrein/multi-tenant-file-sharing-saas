import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.core.deps import get_db
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

    with TestClient(app) as c:
        yield c

    config.settings.UPLOAD_DIR = original_upload_dir
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def tenant(client):
    res = client.post("/api/v1/tenants/", json={"name": "Test Co", "slug": "test-co"})
    return res.json()


@pytest.fixture
def registered_user(client, tenant):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
        "role": "admin",
        "tenant_id": tenant["id"],
    })
    return {"email": "test@example.com", "password": "password123"}


@pytest.fixture
def auth_headers(client, registered_user):
    res = client.post("/api/v1/auth/login", json=registered_user)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
