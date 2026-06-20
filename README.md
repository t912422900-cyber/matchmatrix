# MatchMatrix

MatchMatrix is a private production platform for football and hockey gematria analysis.

## Source Of Truth

Read `MatchMatrix_FINAL_PRD.md` before implementation. Do not split the product PRD into multiple PRD files.

## First Delivery Target

Deploy to `https://matrix.tx-bot.com` behind the existing VPS Nginx reverse proxy.

## Safety Rules

- Do not bind container ports `80` or `443`.
- Do not commit secrets.
- Do not apply Grok recommendations without owner confirmation.
- Do not deploy to VPS without preflight checks.
- Keep public registration and payments disabled until explicitly enabled by the owner.

## Planned Stack

- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: PostgreSQL
- Cache/Queue: Redis
- AI worker: Grok CLI
- Deployment: Docker Compose behind existing Nginx

## Current Project Files

- `MatchMatrix_FINAL_PRD.md` - canonical product PRD.
- `MatchMatrix_CODEX_MASTER_PROMPT.md` - Codex/Hermes implementation prompt.
- `docs/superpowers/plans/2026-06-20-matchmatrix-production-delivery.md` - phased technical implementation plan.
- `infra/docker-compose.yml` - safe local Compose skeleton.
- `infra/nginx/matchmatrix.conf.example` - example reverse-proxy config only.

## Local Verification

```powershell
docker compose -f .\infra\docker-compose.yml config
```

The Compose config must parse without binding public `80/443` ports.
