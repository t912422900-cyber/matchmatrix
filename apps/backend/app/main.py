from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy.orm import Session, sessionmaker

from app.auth.router import router as auth_router
from app.core.config import Settings
from app.db.session import create_engine_from_settings, create_session_factory


def create_app(*, session_factory: sessionmaker[Session] | None = None) -> FastAPI:
    settings = Settings.from_env()
    if session_factory is None:
        engine = create_engine_from_settings(settings)
        session_factory = create_session_factory(engine)

    app = FastAPI(title="MatchMatrix Backend")
    app.state.settings = settings
    app.state.session_factory = session_factory
    app.include_router(auth_router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "matchmatrix-backend"}

    return app
