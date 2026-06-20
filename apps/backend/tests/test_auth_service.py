from datetime import UTC, datetime, timedelta


def test_bootstrap_owner_creates_user_and_totp_secret(db_session, owner_settings):
    from app.auth.service import AuthService
    from app.db.models import TotpSecret, User

    service = AuthService(db_session, owner_settings)

    owner = service.bootstrap_owner()

    stored_owner = db_session.query(User).filter_by(email="owner@example.com").one()
    stored_totp = db_session.query(TotpSecret).filter_by(user_id=stored_owner.id).one()
    assert owner.id == stored_owner.id
    assert stored_owner.role == "owner"
    assert stored_totp.is_confirmed is True
    assert stored_totp.secret_ciphertext == "JBSWY3DPEHPK3PXP"


def test_authenticate_owner_creates_persisted_session(db_session, owner_settings):
    from app.auth.service import AuthService
    from app.auth.totp import generate_totp_code
    from app.db.models import Session

    service = AuthService(db_session, owner_settings)
    service.bootstrap_owner()

    session_token = service.authenticate_owner(
        email="owner@example.com",
        password="correct-password",
        totp_code=generate_totp_code("JBSWY3DPEHPK3PXP"),
        user_agent="pytest",
        ip_address="127.0.0.1",
    )

    stored_session = db_session.query(Session).one()
    assert session_token
    assert stored_session.user_agent == "pytest"
    expires_at = stored_session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    assert expires_at > datetime.now(UTC) + timedelta(hours=7)


def test_get_user_for_session_rejects_revoked_session(db_session, owner_settings):
    from app.auth.service import AuthService
    from app.auth.totp import generate_totp_code
    from app.db.models import Session

    service = AuthService(db_session, owner_settings)
    service.bootstrap_owner()
    session_token = service.authenticate_owner(
        email="owner@example.com",
        password="correct-password",
        totp_code=generate_totp_code("JBSWY3DPEHPK3PXP"),
    )
    stored_session = db_session.query(Session).one()
    stored_session.revoked_at = datetime.now(UTC)
    db_session.commit()

    assert service.get_user_for_session(session_token) is None
