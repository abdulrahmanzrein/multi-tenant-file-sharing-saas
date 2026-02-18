def test_register(client, tenant):
    res = client.post("/api/v1/auth/register", json={
        "email": "new@example.com",
        "password": "pass123",
        "full_name": "New User",
        "role": "member",
        "tenant_id": tenant["id"],
    })
    assert res.status_code == 200
    assert res.json()["email"] == "new@example.com"


def test_register_duplicate_email(client, tenant, registered_user):
    res = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "pass123",
        "full_name": "Duplicate",
        "role": "member",
        "tenant_id": tenant["id"],
    })
    assert res.status_code == 400


def test_login(client, registered_user):
    res = client.post("/api/v1/auth/login", json=registered_user)
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert "refresh_token" in res.json()


def test_login_wrong_password(client, registered_user):
    res = client.post("/api/v1/auth/login", json={
        "email": registered_user["email"],
        "password": "wrongpass",
    })
    assert res.status_code == 401


def test_refresh_token(client, registered_user):
    login_res = client.post("/api/v1/auth/login", json=registered_user)
    refresh_token = login_res.json()["refresh_token"]

    res = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_refresh_with_access_token_fails(client, registered_user):
    login_res = client.post("/api/v1/auth/login", json=registered_user)
    access_token = login_res.json()["access_token"]

    res = client.post("/api/v1/auth/refresh", json={"refresh_token": access_token})
    assert res.status_code == 401
