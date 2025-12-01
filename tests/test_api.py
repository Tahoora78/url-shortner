# tests/test_api.py

def test_create_short_url(client):
    payload = {"original_url": "https://example.com"}
    response = client.post("/shorten", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data

    assert data["original_url"].rstrip("/") == payload["original_url"].rstrip("/")


def test_create_short_url_invalid(client):
    payload = {"original_url": "not-a-url"}
    response = client.post("/shorten", json=payload)
    assert response.status_code == 422


def _get_no_redirect(client, path):
    for kw in ("allow_redirects", "follow_redirects"):
        try:
            return client.get(path, **{kw: False})
        except TypeError:
            continue
    return client.get(path)


def test_redirect_short_url(client):
    payload = {"original_url": "https://example.com/abc"}
    res = client.post("/shorten", json=payload)
    code = res.json()["short_code"]

    redirect_res = _get_no_redirect(client, f"/{code}")
    assert redirect_res.status_code == 307
    assert redirect_res.headers["location"] == payload["original_url"]


def test_redirect_not_found(client):
    res = _get_no_redirect(client, "/unknown123")
    assert res.status_code == 404
