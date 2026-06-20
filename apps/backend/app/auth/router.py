from __future__ import annotations

import base64
import hashlib
import hmac

from fastapi import APIRouter, Cookie, HTTPException, Response, status
from pydantic import BaseModel

from app.auth.security import verify_password
from app.auth.totp import verify_totp_code
from app.core.config import Settings

SESSION_COOKIE_NAME = "matchmatrix_session"

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str
    totp_code: str


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(payload: LoginRequest, response: Response) -> None:
    settings = Settings.from_env()
    _verify_owner_login(settings, payload)
    token = _sign_session(settings.owner_email or payload.email, settings.session_secret)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 8,
    )
    return None


@router.get("/me")
def me(matchmatrix_session: str | None = Cookie(default=None)) -> dict[str, str]:
    settings = Settings.from_env()
    if matchmatrix_session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    email = _verify_session(matchmatrix_session, settings.session_secret)
    if email is None or email != settings.owner_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    return {"email": email, "role": "owner"}


def _verify_owner_login(settings: Settings, payload: LoginRequest) -> None:
    if not settings.owner_email or not settings.owner_password_hash or not settings.owner_totp_secret:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Owner bootstrap is not configured")

    credentials_ok = (
        payload.email == settings.owner_email
        and verify_password(payload.password, settings.owner_password_hash)
        and verify_totp_code(settings.owner_totp_secret, payload.totp_code)
    )
    if not credentials_ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


def _sign_session(email: str, secret: str) -> str:
    email_raw = email.encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), email_raw, hashlib.sha256).digest()
    return "{email}.{signature}".format(
        email=base64.urlsafe_b64encode(email_raw).decode("ascii").rstrip("="),
        signature=base64.urlsafe_b64encode(signature).decode("ascii").rstrip("="),
    )


def _verify_session(token: str, secret: str) -> str | None:
    try:
        email_raw, signature_raw = token.split(".", 1)
        email_bytes = _urlsafe_b64decode(email_raw)
        signature = _urlsafe_b64decode(signature_raw)
    except (ValueError, TypeError):
        return None

    expected = hmac.new(secret.encode("utf-8"), email_bytes, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected):
        return None
    return email_bytes.decode("utf-8")


def _urlsafe_b64decode(value: str) -> bytes:
    padding = "=" * ((4 - len(value) % 4) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))
