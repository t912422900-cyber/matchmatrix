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
