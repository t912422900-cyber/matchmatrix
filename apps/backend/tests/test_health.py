from fastapi.testclient import TestClient


def test_health_endpoint_reports_ok(monkeypatch):
    from app.main import create_app

    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@postgres:5432/matchmatrix")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("SESSION_SECRET", "local-secret")

    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "matchmatrix-backend"}
