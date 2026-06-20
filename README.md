# MatchMatrix

MatchMatrix is a private production platform for football and hockey gematria analysis.

## Source Of Truth

Read `MatchMatrix_FINAL_PRD.md` before implementation. Do not split the product PRD into multiple PRD files.

## First Delivery Target

Run the full product locally from this PC with Docker Compose:

- Frontend: `http://localhost:3100`
- Backend API: `http://localhost:8100`

## Safety Rules

- Do not commit secrets.
- Do not apply Grok recommendations without owner confirmation.
- Do not deploy to VPS; this project is local-only unless the owner changes that decision later.
- Keep public registration and payments disabled until explicitly enabled by the owner.

## Planned Stack

- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: PostgreSQL
- Cache/Queue: Redis
- AI worker: Grok CLI
- Runtime: local Docker Compose on this PC

## Current Project Files

- `MatchMatrix_FINAL_PRD.md` - canonical product PRD.
- `MatchMatrix_CODEX_MASTER_PROMPT.md` - Codex/Hermes implementation prompt.
- `docs/superpowers/plans/2026-06-20-matchmatrix-production-delivery.md` - phased technical implementation plan.
- `infra/docker-compose.yml` - safe local Compose skeleton.

## Local Verification

```powershell
docker compose -f .\infra\docker-compose.yml config
```

The Compose config must parse and expose only localhost development ports.
