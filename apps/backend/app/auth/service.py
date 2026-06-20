from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session as DbSession

from app.auth.security import verify_password
from app.auth.totp import verify_totp_code
from app.core.config import Settings
from app.db.models import Session, TotpSecret, User

SESSION_TTL = timedelta(hours=8)


class AuthService:
    def __init__(self, db: DbSession, settings: Settings) -> None:
        self._db = db
        self._settings = settings

    def bootstrap_owner(self) -> User:
        self._require_owner_bootstrap()
        owner = self._db.query(User).filter_by(email=self._settings.owner_email).one_or_none()
        if owner is None:
            owner = User(
                email=self._settings.owner_email,
                password_hash=self._settings.owner_password_hash,
                role="owner",
                is_active=True,
            )
            self._db.add(owner)
            self._db.flush()

        totp = self._db.query(TotpSecret).filter_by(user_id=owner.id).one_or_none()
        if totp is None:
            totp = TotpSecret(
                user_id=owner.id,
                secret_ciphertext=self._settings.owner_totp_secret,
                is_confirmed=True,
                confirmed_at=datetime.now(UTC),
            )
            self._db.add(totp)

        self._db.commit()
        self._db.refresh(owner)
        return owner

    def authenticate_owner(
        self,
        *,
        email: str,
        password: str,
        totp_code: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> str | None:
        self.bootstrap_owner()
        owner = self._db.query(User).filter_by(email=email, role="owner", is_active=True).one_or_none()
        if owner is None or not verify_password(password, owner.password_hash):
            return None

        totp = self._db.query(TotpSecret).filter_by(user_id=owner.id, is_confirmed=True).one_or_none()
        if totp is None or not verify_totp_code(totp.secret_ciphertext, totp_code):
            return None

        token = secrets.token_urlsafe(48)
        stored_session = Session(
            user_id=owner.id,
            session_hash=_hash_session_token(token),
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.now(UTC) + SESSION_TTL,
        )
        self._db.add(stored_session)
        self._db.commit()
        return token

    def get_user_for_session(self, session_token: str) -> User | None:
        stored_session = (
            self._db.query(Session)
            .filter_by(session_hash=_hash_session_token(session_token))
            .one_or_none()
        )
        if stored_session is None:
            return None
        if stored_session.revoked_at is not None:
            return None
        if _as_aware(stored_session.expires_at) <= datetime.now(UTC):
            return None
        return self._db.get(User, stored_session.user_id)

    def _require_owner_bootstrap(self) -> None:
        missing = [
            name
            for name, value in {
                "OWNER_EMAIL": self._settings.owner_email,
                "OWNER_PASSWORD_HASH": self._settings.owner_password_hash,
                "OWNER_TOTP_SECRET": self._settings.owner_totp_secret,
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(f"Owner bootstrap is missing: {', '.join(missing)}")


def _hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _as_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value
