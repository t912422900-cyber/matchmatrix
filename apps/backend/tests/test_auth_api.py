from fastapi.testclient import TestClient


def _client_with_owner(monkeypatch):
    from app.auth.security import hash_password
    from app.auth.totp import generate_totp_secret
    from app.main import create_app

    totp_secret = generate_totp_secret()
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@postgres:5432/matchmatrix")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("SESSION_SECRET", "local-secret")
    monkeypatch.setenv("OWNER_EMAIL", "owner@example.com")
    monkeypatch.setenv("OWNER_PASSWORD_HASH", hash_password("correct-password"))
    monkeypatch.setenv("OWNER_TOTP_SECRET", totp_secret)

    return TestClient(create_app()), totp_secret


def test_login_rejects_wrong_password(monkeypatch):
    from app.auth.totp import generate_totp_code

    client, totp_secret = _client_with_owner(monkeypatch)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "owner@example.com",
            "password": "wrong-password",
            "totp_code": generate_totp_code(totp_secret),
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_sets_session_cookie_and_me_returns_owner(monkeypatch):
    from app.auth.totp import generate_totp_code

    client, totp_secret = _client_with_owner(monkeypatch)

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "owner@example.com",
            "password": "correct-password",
            "totp_code": generate_totp_code(totp_secret),
        },
    )

    assert login_response.status_code == 204
    assert "matchmatrix_session" in login_response.cookies

    me_response = client.get("/api/auth/me")

    assert me_response.status_code == 200
    assert me_response.json() == {"email": "owner@example.com", "role": "owner"}


def test_me_requires_session(monkeypatch):
    client, _ = _client_with_owner(monkeypatch)

    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}
