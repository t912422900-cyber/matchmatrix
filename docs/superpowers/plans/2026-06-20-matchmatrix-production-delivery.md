# MatchMatrix Production Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build MatchMatrix as a full local production-grade system for private football and hockey gematria analysis, running entirely from the owner's PC.

**Architecture:** MatchMatrix uses a Next.js admin frontend, FastAPI backend, PostgreSQL, Redis, Grok CLI worker, scheduler, and Docker Compose. The app runs locally on this PC through localhost ports and does not require VPS, public DNS, external Nginx, or production TLS.

**Tech Stack:** Next.js, TypeScript, FastAPI, Python 3.12+, PostgreSQL 16+, Redis, Docker Compose, Grok CLI via owner OAuth/Grok Super.

---

## Source Of Truth

- Product PRD: `C:\Users\dimdi\Desktop\all_Project_codex\app_matrix\MatchMatrix_FINAL_PRD.md`
- Obsidian PRD mirror: `C:\Users\dimdi\Documents\ObsidianVault\Projects\MatchMatrix\MatchMatrix_FINAL_PRD.md`
- Master prompt: `C:\Users\dimdi\Desktop\all_Project_codex\app_matrix\MatchMatrix_CODEX_MASTER_PROMPT.md`
- Local Codex instructions: `C:\Users\dimdi\Desktop\all_Project_codex\app_matrix\AGENTS.md`

Do not split the product PRD into multiple PRD files. This implementation plan is a technical execution artifact only.

## Repository Structure

Create and maintain this structure:

```text
app_matrix/
  AGENTS.md
  MatchMatrix_FINAL_PRD.md
  MatchMatrix_CODEX_MASTER_PROMPT.md
  README.md
  .gitignore
  .env.example
  apps/
    frontend/
    backend/
    grok-worker/
    scheduler/
  packages/
    gematria-core/
    shared-types/
  infra/
    docker-compose.yml
    scripts/
      preflight.ps1
      backup.ps1
  docs/
    architecture/
    deployment/
    superpowers/
      plans/
        2026-06-20-matchmatrix-production-delivery.md
```

---

### Task 1: Phase 0 Repository Safety Baseline

**Files:**
- Verify: `AGENTS.md`
- Verify: `MatchMatrix_FINAL_PRD.md`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `README.md`
- Create: `infra/docker-compose.yml`
- Create: `infra/scripts/preflight.ps1`

- [ ] **Step 1: Verify local project instructions exist**

Run:

```powershell
Test-Path .\AGENTS.md
```

Expected: `True`.

- [ ] **Step 2: Verify canonical PRD exists**

Run:

```powershell
Test-Path .\MatchMatrix_FINAL_PRD.md
```

Expected: `True`.

- [ ] **Step 3: Create baseline ignore rules**

Create `.gitignore` with:

```gitignore
.env
.env.*
!.env.example
node_modules/
.next/
dist/
build/
__pycache__/
.pytest_cache/
.venv/
venv/
*.pyc
*.log
*.tmp
postgres-data/
redis-data/
backups/
coverage/
```

- [ ] **Step 4: Create safe environment example**

Create `.env.example` with:

```dotenv
APP_ENV=local
APP_DOMAIN=localhost
FRONTEND_INTERNAL_PORT=3100
BACKEND_INTERNAL_PORT=8100
POSTGRES_DB=matchmatrix
POSTGRES_USER=matchmatrix
POSTGRES_PASSWORD=change-me-local-only
DATABASE_URL=postgresql+psycopg://matchmatrix:change-me-local-only@postgres:5432/matchmatrix
REDIS_URL=redis://redis:6379/0
SESSION_SECRET=change-me
TOTP_ISSUER=MatchMatrix
GROK_CLI_COMMAND=grok
GROK_OAUTH_MODE=owner-session
BACKUP_DIR=/backups
```

- [ ] **Step 5: Create README foundation**

Create `README.md` with sections:

```markdown
# MatchMatrix

MatchMatrix is a private production platform for football and hockey gematria analysis.

## Source Of Truth

Read `MatchMatrix_FINAL_PRD.md` before implementation.

## First Delivery Target

Run locally from this PC:

- Frontend: `http://localhost:3100`
- Backend API: `http://localhost:8100`

## Safety Rules

- Do not commit secrets.
- Do not apply Grok recommendations without owner confirmation.
- Do not deploy to VPS unless the owner explicitly changes the local-only decision later.

## Planned Stack

- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: PostgreSQL
- Cache/Queue: Redis
- AI worker: Grok CLI
- Runtime: local Docker Compose on this PC
```

- [ ] **Step 6: Create Docker Compose skeleton**

Create `infra/docker-compose.yml` with services for `frontend`, `backend`, `postgres`, `redis`, `grok-worker`, and `scheduler`. Containers must expose only internal ports and bind frontend/backend to localhost in local/dev mode.

- [ ] **Step 7: Create local preflight script**

Create `infra/scripts/preflight.ps1` to print:

```powershell
docker ps
docker compose -f .\infra\docker-compose.yml config
netstat -ano -p tcp
```

Expected: script reports current local state but does not change machine configuration.

- [ ] **Step 8: Verify Phase 0**

Run:

```powershell
docker compose -f .\infra\docker-compose.yml config
```

Expected: Compose config parses without errors.

---

### Task 2: Phase 1 Backend, Database, Auth, And 2FA

**Files:**
- Create: `apps/backend/`
- Create: `apps/backend/app/main.py`
- Create: `apps/backend/app/core/config.py`
- Create: `apps/backend/app/auth/`
- Create: `apps/backend/app/db/`
- Create: `apps/backend/tests/`

- [ ] **Step 1: Scaffold FastAPI backend**

Create a Python backend with FastAPI, Pydantic settings, SQLAlchemy/Alembic, pytest, and healthcheck routes.

- [ ] **Step 2: Add env validation**

Backend startup must fail with a clear error when `DATABASE_URL`, `REDIS_URL`, or `SESSION_SECRET` is missing.

- [ ] **Step 3: Add auth models**

Create tables for `users`, `sessions`, `totp_secrets`, and `audit_logs`.

- [ ] **Step 4: Implement login/session/2FA**

Implement owner login with password hash, secure session cookie, and TOTP verification.

- [ ] **Step 5: Verify Phase 1**

Run:

```powershell
pytest apps/backend/tests -q
```

Expected: auth, config, and health tests pass.

---

### Task 3: Phase 2 Match Management And Fact Assistant

**Files:**
- Create: `apps/backend/app/matches/`
- Create: `apps/backend/app/fact_assistant/`
- Create: `apps/backend/tests/test_matches.py`
- Create: `apps/backend/tests/test_fact_assistant.py`

- [ ] **Step 1: Implement match schema**

Add tables for sports, teams, tournaments, venues, matches, match participants, referees, VAR, and match results.

- [ ] **Step 2: Implement manual match CRUD**

Owner can create, edit, view, and delete draft matches through API.

- [ ] **Step 3: Implement data quality status**

Incomplete matches are allowed but receive `data_quality` and missing-field details.

- [ ] **Step 4: Implement web-fact assistant draft flow**

Fact assistant stores found candidate facts as drafts. It must not overwrite match data until confirmed by owner.

- [ ] **Step 5: Verify Phase 2**

Run:

```powershell
pytest apps/backend/tests/test_matches.py apps/backend/tests/test_fact_assistant.py -q
```

Expected: match CRUD, incomplete data handling, and fact confirmation tests pass.

---

### Task 4: Phase 3 Gematria Engine With 30 Working Models

**Files:**
- Create: `packages/gematria-core/`
- Create: `packages/gematria-core/models/`
- Create: `packages/gematria-core/tests/`
- Create: `apps/backend/app/analysis/`

- [ ] **Step 1: Implement normalization**

Support English and Russian language layers as separate calculation inputs.

- [ ] **Step 2: Implement all 30 models**

Implement the 30 models listed in `MatchMatrix_FINAL_PRD.md` section `20. 30 Gematria Models`.

- [ ] **Step 3: Implement full trace**

Every calculation must store language, normalized input, symbols, symbol values, intermediate sums, raw score, normalized score, direction, confidence, model version, and weight.

- [ ] **Step 4: Implement analysis snapshot**

Each analysis run stores a snapshot of match data and active model settings.

- [ ] **Step 5: Verify Phase 3**

Run:

```powershell
pytest packages/gematria-core/tests apps/backend/tests/test_analysis.py -q
```

Expected: all 30 model tests pass and snapshot/trace tests pass.

---

### Task 5: Phase 4 Admin UI And Full-Screen Match Review

**Files:**
- Create: `apps/frontend/`
- Create: `apps/frontend/app/`
- Create: `apps/frontend/components/`
- Create: `apps/frontend/tests/`

- [ ] **Step 1: Scaffold Next.js frontend**

Use TypeScript, App Router, Tailwind, TanStack Query, and a restrained premium dark visual system.

- [ ] **Step 2: Implement login and 2FA screens**

Owner can log in and pass TOTP before seeing dashboard.

- [ ] **Step 3: Implement dashboard queue**

Show up to 10 active matches ordered by work state: missing data, ready for pre-match, waiting result, waiting post-match, recently completed.

- [ ] **Step 4: Implement full-screen match analysis modal**

Modal shows summary, language layers, all 30 model outputs, trace drilldown, weights, Grok analysis, post-match comparison, match notes, and model notes.

- [ ] **Step 5: Verify Phase 4**

Run:

```powershell
npm test --workspaces
```

Expected: frontend unit tests pass.

Run browser smoke checks against the local app before calling the UI complete.

---

### Task 6: Phase 5 Grok CLI Center And Learning Workflow

**Files:**
- Create: `apps/grok-worker/`
- Create: `apps/backend/app/grok/`
- Create: `apps/backend/app/learning/`
- Create: `apps/backend/tests/test_grok.py`
- Create: `apps/backend/tests/test_learning.py`

- [ ] **Step 1: Implement Grok job queue**

Backend creates Grok jobs for manual runs and post-match runs.

- [ ] **Step 2: Implement Grok worker adapter**

Worker calls the configured `GROK_CLI_COMMAND` and stores outputs as drafts.

- [ ] **Step 3: Implement recommendation approval flow**

Grok can recommend changes, but backend applies them only after explicit owner approval.

- [ ] **Step 4: Implement 10-match language review**

After each 10 completed matches, Grok receives stats comparing English and Russian language layers.

- [ ] **Step 5: Verify Phase 5**

Run:

```powershell
pytest apps/backend/tests/test_grok.py apps/backend/tests/test_learning.py -q
```

Expected: Grok draft, approval, rejection, and 10-match language review tests pass.

---

### Task 7: Phase 6 Statistics, Retro-Test, And Version History

**Files:**
- Create: `apps/backend/app/statistics/`
- Create: `apps/backend/app/retrotest/`
- Create: `apps/backend/app/versioning/`

- [ ] **Step 1: Implement model statistics**

Track exact, partial, wrong, no_signal, confidence calibration, sport, tournament, and last 10/30/100 match windows.

- [ ] **Step 2: Implement retro-test**

Retro-test historical matches without mutating production weights.

- [ ] **Step 3: Implement version history**

Store model, weight, prompt, and recommendation versions with rollback drafts requiring confirmation.

- [ ] **Step 4: Verify Phase 6**

Run:

```powershell
pytest apps/backend/tests/test_statistics.py apps/backend/tests/test_retrotest.py apps/backend/tests/test_versioning.py -q
```

Expected: statistics, retro-test, and version history tests pass.

---

### Task 8: Phase 7 Local Backup, Hardening, And Runbook

**Files:**
- Create: `infra/scripts/backup.ps1`
- Create: `docs/deployment/local-preflight.md`
- Create: `docs/deployment/local-runbook.md`

- [ ] **Step 1: Implement manual backup**

Backup script dumps PostgreSQL and archives uploaded/configured runtime data without including secrets in repo.

- [ ] **Step 2: Write local preflight checklist**

Document checks for Docker availability, localhost ports, volumes, env files, Grok CLI availability, and backup destination.

- [ ] **Step 3: Write local run procedure**

The runbook must start, stop, backup, restore, and verify MatchMatrix locally without touching VPS infrastructure.

- [ ] **Step 4: Verify Phase 7 locally**

Run:

```powershell
docker compose -f .\infra\docker-compose.yml config
```

Expected: Compose config is valid.

Expected: Compose config is valid and only localhost app ports are exposed.

---

### Task 9: Phase 8 Monetization Readiness

**Files:**
- Create: `apps/backend/app/billing/`
- Create: `apps/backend/app/limits/`

- [ ] **Step 1: Add billing-ready schema**

Add plans, subscriptions, usage limits, and API users without enabling public signup.

- [ ] **Step 2: Add feature flags**

Public registration, checkout, and API user access remain disabled until owner explicitly enables them.

- [ ] **Step 3: Verify Phase 8**

Run:

```powershell
pytest apps/backend/tests/test_billing_readiness.py apps/backend/tests/test_feature_flags.py -q
```

Expected: billing-ready tables exist and public access remains disabled by default.

---

## Final Verification Before Production Claim

Run all checks:

```powershell
pytest apps/backend/tests packages/gematria-core/tests -q
npm test --workspaces
docker compose -f .\infra\docker-compose.yml config
```

Run secret scan:

```powershell
rg -n --hidden --glob '!.git' --glob '!node_modules' --glob '!dist' --glob '!build' "(api[_-]?key|secret|token|password|BEGIN PRIVATE KEY|xoxb-|ghp_|sk-)" .
```

Expected: no real secrets. `.env.example` placeholder values are acceptable.

Production readiness requires:

- the owner can complete the full match workflow from `http://localhost:3100`;
- no VPS, public DNS, or external Nginx is required;
- Grok recommendations never apply without confirmation;
- manual backup works;
- all tests and preflight checks pass.
