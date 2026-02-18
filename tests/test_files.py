import io


def test_upload_file(client, auth_headers):
    res = client.post(
        "/api/v1/files/upload",
        files={"upload": ("test.txt", io.BytesIO(b"hello world"), "text/plain")},
        headers=auth_headers,
    )
    assert res.status_code == 201
    assert res.json()["original_filename"] == "test.txt"
    assert res.json()["size"] == 11


def test_list_files(client, auth_headers):
    client.post(
        "/api/v1/files/upload",
        files={"upload": ("a.txt", io.BytesIO(b"aaa"), "text/plain")},
        headers=auth_headers,
    )
    res = client.get("/api/v1/files/", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_file(client, auth_headers):
    upload = client.post(
        "/api/v1/files/upload",
        files={"upload": ("doc.pdf", io.BytesIO(b"pdf content"), "application/pdf")},
        headers=auth_headers,
    )
    file_id = upload.json()["id"]

    res = client.get(f"/api/v1/files/{file_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["original_filename"] == "doc.pdf"


def test_download_file(client, auth_headers):
    upload = client.post(
        "/api/v1/files/upload",
        files={"upload": ("data.txt", io.BytesIO(b"file data"), "text/plain")},
        headers=auth_headers,
    )
    file_id = upload.json()["id"]

    res = client.get(f"/api/v1/files/{file_id}/download", headers=auth_headers)
    assert res.status_code == 200
    assert res.content == b"file data"


def test_delete_file(client, auth_headers):
    upload = client.post(
        "/api/v1/files/upload",
        files={"upload": ("del.txt", io.BytesIO(b"bye"), "text/plain")},
        headers=auth_headers,
    )
    file_id = upload.json()["id"]

    res = client.delete(f"/api/v1/files/{file_id}", headers=auth_headers)
    assert res.status_code == 204

    res = client.get(f"/api/v1/files/{file_id}", headers=auth_headers)
    assert res.status_code == 404


def test_file_tenant_isolation(client, tenant, auth_headers):
    upload = client.post(
        "/api/v1/files/upload",
        files={"upload": ("private.txt", io.BytesIO(b"secret"), "text/plain")},
        headers=auth_headers,
    )
    file_id = upload.json()["id"]

    tenant2 = client.post("/api/v1/tenants/", json={"name": "Other Co", "slug": "other-co"}).json()
    client.post("/api/v1/auth/register", json={
        "email": "other@example.com",
        "password": "pass123",
        "full_name": "Other User",
        "role": "member",
        "tenant_id": tenant2["id"],
    })
    login2 = client.post("/api/v1/auth/login", json={"email": "other@example.com", "password": "pass123"})
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    res = client.get(f"/api/v1/files/{file_id}", headers=headers2)
    assert res.status_code == 404
