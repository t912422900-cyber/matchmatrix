from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


def _client_with_owner(monkeypatch):
    from app.auth.security import hash_password
    from app.auth.totp import generate_totp_secret
    from app.db.base import Base
    from app.db import models  # noqa: F401
    from app.main import create_app

    totp_secret = generate_totp_secret()
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("SESSION_SECRET", "local-secret")
    monkeypatch.setenv("OWNER_EMAIL", "owner@example.com")
    monkeypatch.setenv("OWNER_PASSWORD_HASH", hash_password("correct-password"))
    monkeypatch.setenv("OWNER_TOTP_SECRET", totp_secret)

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    return TestClient(create_app(session_factory=session_factory)), totp_secret, session_factory


def test_login_rejects_wrong_password(monkeypatch):
    from app.auth.totp import generate_totp_code

    client, totp_secret, _ = _client_with_owner(monkeypatch)

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

    client, totp_secret, session_factory = _client_with_owner(monkeypatch)

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

    from app.db.models import Session

    with session_factory() as db:
        assert db.query(Session).count() == 1

    me_response = client.get("/api/auth/me")

    assert me_response.status_code == 200
    assert me_response.json() == {"email": "owner@example.com", "role": "owner"}


def test_me_requires_session(monkeypatch):
    client, _, _ = _client_with_owner(monkeypatch)

    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}
