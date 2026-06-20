from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    session_secret: str
    backend_port: int = 8100
    totp_issuer: str = "MatchMatrix"
    owner_email: str | None = None
    owner_password_hash: str | None = None
    owner_totp_secret: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        database_url = _required_env("DATABASE_URL")
        redis_url = _required_env("REDIS_URL")
        session_secret = _required_env("SESSION_SECRET")
        backend_port = int(os.getenv("BACKEND_PORT", "8100"))
        totp_issuer = os.getenv("TOTP_ISSUER", "MatchMatrix")
        owner_email = os.getenv("OWNER_EMAIL")
        owner_password_hash = os.getenv("OWNER_PASSWORD_HASH")
        owner_totp_secret = os.getenv("OWNER_TOTP_SECRET")

        return cls(
            database_url=database_url,
            redis_url=redis_url,
            session_secret=session_secret,
            backend_port=backend_port,
            totp_issuer=totp_issuer,
            owner_email=owner_email,
            owner_password_hash=owner_password_hash,
            owner_totp_secret=owner_totp_secret,
        )


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ValueError(f"{name} is required")
    return value
