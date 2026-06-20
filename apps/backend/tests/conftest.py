import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.security import hash_password
from app.core.config import Settings
from app.db.base import Base
from app.db import models  # noqa: F401


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    with session_factory() as session:
        yield session


@pytest.fixture()
def owner_settings():
    return Settings(
        database_url="sqlite+pysqlite:///:memory:",
        redis_url="redis://redis:6379/0",
        session_secret="local-secret",
        owner_email="owner@example.com",
        owner_password_hash=hash_password("correct-password"),
        owner_totp_secret="JBSWY3DPEHPK3PXP",
    )
