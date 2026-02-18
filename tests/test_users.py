def test_get_me(client, auth_headers):
    res = client.get("/api/v1/users/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"


def test_get_me_no_auth(client):
    res = client.get("/api/v1/users/me")
    assert res.status_code == 401


def test_update_name(client, auth_headers):
    res = client.put("/api/v1/users/me", json={"full_name": "Updated Name"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["full_name"] == "Updated Name"


def test_update_email_taken(client, tenant, auth_headers):
    client.post("/api/v1/auth/register", json={
        "email": "other@example.com",
        "password": "pass123",
        "full_name": "Other",
        "role": "member",
        "tenant_id": tenant["id"],
    })
    res = client.put("/api/v1/users/me", json={"email": "other@example.com"}, headers=auth_headers)
    assert res.status_code == 400


def test_delete_me(client, auth_headers):
    res = client.delete("/api/v1/users/me", headers=auth_headers)
    assert res.status_code == 204

    res = client.get("/api/v1/users/me", headers=auth_headers)
    assert res.status_code == 401
