def test_engine_factory_uses_configured_database_url(monkeypatch):
    from app.core.config import Settings
    from app.db.session import create_engine_from_settings

    settings = Settings(
        database_url="sqlite+pysqlite:///:memory:",
        redis_url="redis://redis:6379/0",
        session_secret="local-secret",
    )

    engine = create_engine_from_settings(settings)

    assert str(engine.url) == "sqlite+pysqlite:///:memory:"


def test_session_factory_creates_sessions(monkeypatch):
    from app.core.config import Settings
    from app.db.session import create_engine_from_settings, create_session_factory

    settings = Settings(
        database_url="sqlite+pysqlite:///:memory:",
        redis_url="redis://redis:6379/0",
        session_secret="local-secret",
    )
    engine = create_engine_from_settings(settings)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        assert session.bind is engine
