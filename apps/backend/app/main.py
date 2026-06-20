from __future__ import annotations

from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.core.config import Settings


def create_app() -> FastAPI:
    Settings.from_env()
    app = FastAPI(title="MatchMatrix Backend")
    app.include_router(auth_router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "matchmatrix-backend"}

    return app
