# MatchMatrix Backend

FastAPI backend for MatchMatrix.

## Local Commands

Run tests:

```powershell
pytest apps/backend/tests -q
```

Render migration SQL without connecting to PostgreSQL:

```powershell
Push-Location apps/backend
$env:DATABASE_URL='postgresql+psycopg://matchmatrix:change-me-local-only@postgres:5432/matchmatrix'
$env:REDIS_URL='redis://redis:6379/0'
$env:SESSION_SECRET='change-me'
alembic upgrade head --sql
Pop-Location
```

## Owner Bootstrap

The first private admin account is bootstrapped from environment variables:

```dotenv
OWNER_EMAIL=owner@example.com
OWNER_PASSWORD_HASH=generated-pbkdf2-hash
OWNER_TOTP_SECRET=generated-base32-secret
```

The service stores the owner, confirmed TOTP secret, and login sessions in PostgreSQL. `/api/auth/login` creates a persisted session token, and `/api/auth/me` resolves the owner from that persisted session. Use placeholder values only in `.env.example`.
