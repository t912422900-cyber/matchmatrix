from __future__ import annotations

from collections.abc import Generator

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session as DbSession

from app.auth.service import AuthService
from app.core.config import Settings

SESSION_COOKIE_NAME = "matchmatrix_session"

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str
    totp_code: str


def get_db(request: Request) -> Generator[DbSession, None, None]:
    session_factory = request.app.state.session_factory
    with session_factory() as db:
        yield db


def get_auth_service(request: Request, db: DbSession = Depends(get_db)) -> AuthService:
    settings: Settings = request.app.state.settings
    return AuthService(db, settings)


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(
    payload: LoginRequest,
    response: Response,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    session_token = auth_service.authenticate_owner(
        email=payload.email,
        password=payload.password,
        totp_code=payload.totp_code,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    if session_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 8,
    )
    return None


@router.get("/me")
def me(
    matchmatrix_session: str | None = Cookie(default=None),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    if matchmatrix_session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    user = auth_service.get_user_for_session(matchmatrix_session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    return {"email": user.email, "role": user.role}
