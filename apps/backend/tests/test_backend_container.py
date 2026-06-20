from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parents[1]


def test_backend_dockerfile_exists_and_runs_uvicorn():
    dockerfile = BACKEND_ROOT / "Dockerfile"

    assert dockerfile.exists()

    text = dockerfile.read_text(encoding="utf-8")

    assert "python:3.12-slim" in text
    assert "uvicorn" in text
    assert "app.main:create_app" in text


def test_compose_builds_backend_from_local_dockerfile():
    compose = REPO_ROOT / "infra" / "docker-compose.yml"
    text = compose.read_text(encoding="utf-8")

    assert "dockerfile: apps/backend/Dockerfile" in text
    assert "target: runtime" in text
