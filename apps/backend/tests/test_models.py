def test_auth_foundation_tables_are_declared():
    from app.db.models import AuditLog, Session, TotpSecret, User

    assert User.__tablename__ == "users"
    assert Session.__tablename__ == "sessions"
    assert TotpSecret.__tablename__ == "totp_secrets"
    assert AuditLog.__tablename__ == "audit_logs"
