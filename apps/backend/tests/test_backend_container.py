from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parents[1]


def test_backend_dockerfile_exists_and_uses_start_script():
    dockerfile = BACKEND_ROOT / "Dockerfile"

    assert dockerfile.exists()

    text = dockerfile.read_text(encoding="utf-8")

    assert "python:3.12-slim" in text
    assert "scripts/start.sh" in text
    assert 'CMD ["./scripts/start.sh"]' in text


def test_backend_start_script_runs_migrations_before_uvicorn():
    start_script = BACKEND_ROOT / "scripts" / "start.sh"

    assert start_script.exists()

    text = start_script.read_text(encoding="utf-8")

    assert "alembic upgrade head" in text
    assert "uvicorn app.main:create_app --factory" in text
    assert text.index("alembic upgrade head") < text.index("uvicorn app.main:create_app --factory")


def test_compose_builds_backend_from_local_dockerfile():
    compose = REPO_ROOT / "infra" / "docker-compose.yml"
    text = compose.read_text(encoding="utf-8")

    assert "dockerfile: apps/backend/Dockerfile" in text
    assert "target: runtime" in text
