from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_alembic_configuration_exists():
    assert (BACKEND_ROOT / "alembic.ini").exists()
    assert (BACKEND_ROOT / "alembic" / "env.py").exists()


def test_initial_migration_declares_auth_foundation_tables():
    migration_files = sorted((BACKEND_ROOT / "alembic" / "versions").glob("*.py"))

    assert migration_files, "expected at least one Alembic migration"

    migration_text = "\n".join(path.read_text(encoding="utf-8") for path in migration_files)

    for table_name in ["users", "sessions", "totp_secrets", "audit_logs"]:
        assert f'op.create_table("{table_name}"' in migration_text


def test_alembic_env_uses_sqlalchemy_metadata():
    env_text = (BACKEND_ROOT / "alembic" / "env.py").read_text(encoding="utf-8")

    assert "from app.db.base import Base" in env_text
    assert "target_metadata = Base.metadata" in env_text
