from app.models.tenant import Tenant
from tests.conftest import TestingSessionLocal


def test_list_tenants_requires_auth(client):
    res = client.get("/api/v1/tenants/")
    assert res.status_code == 401


def test_list_tenants_requires_admin(client, tenant):
    # Register a member (not admin) and log them in
    client.post("/api/v1/auth/register", json={
        "email": "member@example.com",
        "password": "pass123",
        "full_name": "Member User",
        "role": "member",
        "tenant_id": tenant["id"],
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "member@example.com",
        "password": "pass123",
    })
    member_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    res = client.get("/api/v1/tenants/", headers=member_headers)
    assert res.status_code == 403


def test_list_tenants_as_admin(client, tenant, admin_headers):
    res = client.get("/api/v1/tenants/", headers=admin_headers)
    assert res.status_code == 200


def test_get_own_tenant(client, tenant, admin_headers):
    res = client.get(f"/api/v1/tenants/{tenant['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["id"] == tenant["id"]


def test_get_other_tenant_denied(client, tenant, auth_headers):
    # Create a second tenant directly in DB
    db = TestingSessionLocal()
    try:
        t2 = Tenant(name="Other Co", slug="other-co")
        db.add(t2)
        db.commit()
        db.refresh(t2)
        other_id = str(t2.id)
    finally:
        db.close()

    # Try to access it with tenant 1's token — should be blocked
    res = client.get(f"/api/v1/tenants/{other_id}", headers=auth_headers)
    assert res.status_code == 403


def test_get_tenant_requires_auth(client, tenant):
    res = client.get(f"/api/v1/tenants/{tenant['id']}")
    assert res.status_code == 401
