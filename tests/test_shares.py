import io
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

from tests.conftest import TestingSessionLocal


def _upload_file(client, auth_headers):
    res = client.post(
        "/api/v1/files/upload",
        files={"upload": ("share_test.txt", io.BytesIO(b"shareable content"), "text/plain")},
        headers=auth_headers,
    )
    return res.json()["id"]


def test_create_share_link(client, auth_headers):
    file_id = _upload_file(client, auth_headers)

    res = client.post(f"/api/v1/files/{file_id}/share", headers=auth_headers)
    assert res.status_code == 200
    assert "token" in res.json()
    assert len(res.json()["token"]) == 64


def test_download_via_share_link(client, auth_headers):
    file_id = _upload_file(client, auth_headers)

    share_res = client.post(f"/api/v1/files/{file_id}/share", headers=auth_headers)
    token = share_res.json()["token"]

    res = client.get(f"/api/v1/share/{token}")
    assert res.status_code == 200
    assert res.content == b"shareable content"


def test_invalid_token_returns_404(client, auth_headers):
    res = client.get("/api/v1/share/notarealtoken")
    assert res.status_code == 404


def test_expired_link_returns_410(client, auth_headers):
    file_id = _upload_file(client, auth_headers)

    past = quote((datetime.now(timezone.utc) - timedelta(hours=1)).isoformat())
    share_res = client.post(
        f"/api/v1/files/{file_id}/share?expires_at={past}",
        headers=auth_headers,
    )
    token = share_res.json()["token"]

    res = client.get(f"/api/v1/share/{token}")
    assert res.status_code == 410
