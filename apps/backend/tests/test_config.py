import pytest


def test_settings_require_database_url(monkeypatch):
    from app.core.config import Settings

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("SESSION_SECRET", "local-secret")

    with pytest.raises(ValueError, match="DATABASE_URL is required"):
        Settings.from_env()


def test_settings_require_redis_url(monkeypatch):
    from app.core.config import Settings

    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@postgres:5432/matchmatrix")
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.setenv("SESSION_SECRET", "local-secret")

    with pytest.raises(ValueError, match="REDIS_URL is required"):
        Settings.from_env()


def test_settings_require_session_secret(monkeypatch):
    from app.core.config import Settings

    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@postgres:5432/matchmatrix")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.delenv("SESSION_SECRET", raising=False)

    with pytest.raises(ValueError, match="SESSION_SECRET is required"):
        Settings.from_env()


def test_settings_load_required_values_and_default_port(monkeypatch):
    from app.core.config import Settings

    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@postgres:5432/matchmatrix")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("SESSION_SECRET", "local-secret")
    monkeypatch.delenv("BACKEND_PORT", raising=False)

    settings = Settings.from_env()

    assert settings.database_url == "postgresql+psycopg://user:pass@postgres:5432/matchmatrix"
    assert settings.redis_url == "redis://redis:6379/0"
    assert settings.session_secret == "local-secret"
    assert settings.backend_port == 8100
    assert settings.totp_issuer == "MatchMatrix"
