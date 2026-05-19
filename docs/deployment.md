# SHNOOR Backend — Render + Neon Deployment Guide

Production deployment for the FastAPI async backend on **Render**, with **Neon PostgreSQL**.

---

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Why Python 3.12 on Render (not 3.14)](#why-python-312-on-render-not-314)
3. [Why FastAPI uses ASGI (not gunicorn WSGI)](#why-fastapi-uses-asgi-not-gunicorn-wsgi)
4. [Prerequisites](#prerequisites)
5. [Neon PostgreSQL setup](#neon-postgresql-setup)
6. [Render web service setup](#render-web-service-setup)
7. [Environment variables](#environment-variables)
8. [GitHub auto-deploy](#github-auto-deploy)
9. [Migrations on deploy](#migrations-on-deploy)
10. [Health checks](#health-checks)
11. [CORS for production](#cors-for-production)
12. [Local development vs production](#local-development-vs-production)
13. [Troubleshooting](#troubleshooting)
14. [Command reference](#command-reference)

---

## Architecture overview

```
GitHub (main) ──auto-deploy──► Render Web Service (Python 3.12)
                                      │
                                      │ asyncpg + SQLAlchemy
                                      ▼
                              Neon PostgreSQL (sslmode=require)
```

| Component | Technology |
|-----------|------------|
| API | FastAPI (ASGI) |
| Server | Uvicorn |
| DB | PostgreSQL via Neon |
| ORM | SQLAlchemy 2.0 async |
| Driver | asyncpg |
| Migrations | Alembic |
| Config | Pydantic Settings |

---

## Why Python 3.12 on Render (not 3.14)

You may run **Python 3.14.4** locally. Production on Render uses **3.12.8** (see `runtime.txt` and `.python-version`).

| Concern | Python 3.14 | Python 3.12 |
|---------|-------------|-------------|
| Native wheels (asyncpg, cryptography) | Newer; occasional build-from-source failures | Mature; prebuilt wheels on Linux |
| Render ecosystem | Supported but newest | Long-term stable default |
| Dependency pins | More likely to break on auto-deploy | Predictable with pinned `requirements.txt` |

**Stability beats bleeding-edge in production.** A failed deploy from a missing C extension is worse than running a proven Python release. Local 3.14 remains supported via `requires-python = ">=3.12,<3.15"` in `pyproject.toml`.

Set on Render:

```bash
PYTHON_VERSION=3.12.8
```

---

## Why FastAPI uses ASGI (not gunicorn WSGI)

Render’s Python template often suggests:

```bash
gunicorn your_application.wsgi   # WRONG for this project
```

| | WSGI (Django/Flask) | ASGI (FastAPI) |
|--|---------------------|----------------|
| Protocol | Synchronous | Async (WebSockets, async DB) |
| Server | gunicorn | **uvicorn** (or gunicorn + UvicornWorker) |
| Entry | `wsgi.py` | `app.main:app` |

This backend uses **async SQLAlchemy + asyncpg**. The correct start command is:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

`$PORT` is injected by Render.

---

## Prerequisites

- [Render](https://render.com) account
- [Neon](https://neon.tech) account
- GitHub repo connected to Render
- Domain for frontend (or Render static site URL) for CORS

---

## Neon PostgreSQL setup

### 1. Create a Neon project

1. Sign in at [neon.tech](https://neon.tech)
2. **New Project** → choose region close to Render (e.g. `us-west-2` for Oregon)
3. Copy the **connection string** (pooled recommended for serverless)

### 2. Connection string format

Neon provides:

```text
postgresql://USER:PASSWORD@ep-xxxx.us-west-2.aws.neon.tech/neondb?sslmode=require
```

The app automatically:

- Converts `postgresql://` → `postgresql+asyncpg://`
- Maps `sslmode=require` → `connect_args={"ssl": True}` for asyncpg

You do **not** need to manually add `+asyncpg` in Render env vars.

### 3. Run migrations (first time)

Locally with production `DATABASE_URL`:

```bash
cd backend
# Windows PowerShell
$env:DATABASE_URL="postgresql://...@neon.tech/neondb?sslmode=require"
alembic upgrade head
```

Or let the Render **build command** run migrations on each deploy (configured in `render.yaml`).

---

## Render web service setup

### Option A — Blueprint (`render.yaml`)

1. Render Dashboard → **New** → **Blueprint**
2. Connect repo; Render reads `backend/render.yaml`
3. Fill **sync: false** secrets in the dashboard after creation

### Option B — Manual web service

| Setting | Value |
|---------|-------|
| **Name** | `e-commerce-backend` |
| **Language** | Python 3 |
| **Branch** | `main` |
| **Region** | Oregon (US West) |
| **Root Directory** | `backend` |
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt && alembic upgrade head` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Health Check Path** | `/health` |

**Do not use** `poetry install` or `gunicorn ... wsgi` unless you intentionally add Poetry/gunicorn to the stack.

---

## Environment variables

Set in **Render Dashboard → Environment**:

| Variable | Required | Example / notes |
|----------|----------|-----------------|
| `PYTHON_VERSION` | Yes | `3.12.8` |
| `APP_ENV` | Yes | `production` |
| `APP_DEBUG` | Yes | `false` |
| `LOG_LEVEL` | No | `INFO` |
| `DATABASE_URL` | Yes | Neon URL with `?sslmode=require` |
| `SECRET_KEY` | Yes | `openssl rand -hex 32` |
| `JWT_SECRET_KEY` | Recommended | Separate from `SECRET_KEY` |
| `JWT_REFRESH_SECRET_KEY` | Optional | Falls back to `JWT_SECRET_KEY` |
| `FRONTEND_URL` | Yes | `https://your-app.onrender.com` |
| `CORS_ORIGINS` | Yes | `https://your-frontend.com` (comma-separated) |
| `GOOGLE_CLIENT_ID` | If OAuth | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | If OAuth | |
| `GOOGLE_REDIRECT_URI` | If OAuth | `https://your-api.onrender.com/api/v1/auth/google/callback` |
| `CLOUDINARY_*` | If uploads | |

See `.env.example` for the full list.

### Fail-fast validation

When `APP_ENV=production`, startup **exits** if:

- `DATABASE_URL` is missing
- `SECRET_KEY` is weak or default
- `APP_DEBUG=true`
- `CORS_ORIGINS` contains `*`

Check **Logs** in Render immediately after deploy.

---

## GitHub auto-deploy

1. Connect repository in Render service settings
2. Enable **Auto-Deploy** for `main`
3. Each push runs: install → migrate → start

**Stability practices:**

- Production deps pinned in `requirements.txt` (exact versions)
- Dev tools in `requirements-dev.txt` (not installed on Render)
- Migrations run in build step before the new instance starts

---

## Migrations on deploy

Build command includes:

```bash
alembic upgrade head
```

Manual migration from local machine:

```bash
cd backend
alembic current
alembic upgrade head
alembic history
```

PowerShell helper: `.\scripts\migrate.ps1`  
Bash helper: `./scripts/migrate.sh`

---

## Health checks

| Path | Purpose |
|------|---------|
| `GET /health` | **Render health check** — API + DB probe |
| `GET /api/v1/health` | Same check under API prefix |
| `GET /api/v1/health/live` | Liveness only (no DB) |
| `GET /api/v1/status` | Detailed API + DB status |

Successful `/health` response:

```json
{
  "status": "ok",
  "version": "0.2.0",
  "timestamp": "2026-05-19T12:00:00+00:00",
  "database": "connected"
}
```

If `database` is `error`, the service may still start in development but **production startup fails** on DB connection errors.

---

## CORS for production

Set comma-separated origins (no wildcard):

```bash
CORS_ORIGINS=https://shnoor.com,https://www.shnoor.com
FRONTEND_URL=https://shnoor.com
```

`ALLOWED_ORIGINS` is an alias merged into `CORS_ORIGINS`.

Local development defaults include `http://localhost:5173`.

---

## Local development vs production

| | Local | Render |
|--|-------|--------|
| Python | 3.14.4 OK | 3.12.8 |
| Env file | `.env` | Dashboard env vars |
| Docs | `/docs` enabled | Disabled (`APP_ENV=production`) |
| DB | Local Postgres or Neon | Neon |
| Start | `uvicorn app.main:app --reload` | `uvicorn ... --port $PORT` |

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload
```

---

## Troubleshooting

### Build fails: `asyncpg` / compiler errors

- Confirm `PYTHON_VERSION=3.12.8`
- Do not use Python 3.14 on Render until all wheels are verified

### `ModuleNotFoundError` on deploy

- **Root Directory** must be `backend`
- Build must use `pip install -r requirements.txt`

### Database SSL errors

- Neon URL must include `?sslmode=require`
- Do not strip query params manually

### `Startup configuration error`

- Read Render logs for the exact validation message
- Set strong `SECRET_KEY` (32+ chars)

### Health check failing

- Path must be `/health` (not `/api/v1/health` unless you change Render settings)
- DB must be reachable from Render (Neon project not suspended)

### OAuth redirect mismatch

- `GOOGLE_REDIRECT_URI` must exactly match Google Console authorized URI
- Use HTTPS Render URL in production

### Migrations fail on build

- Run `alembic upgrade head` locally against Neon to see the error
- Ensure `DATABASE_URL` is set in Render **before** first deploy

---

## Command reference

```bash
# Install production deps
pip install -r requirements.txt

# Install dev deps
pip install -r requirements-dev.txt

# Run API locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Tests
pytest
RUN_DB_TESTS=1 pytest tests/test_status.py

# Generate secret
openssl rand -hex 32
```

### Render-equivalent local start

```bash
# Simulate Render PORT
$env:PORT=8000; uvicorn app.main:app --host 0.0.0.0 --port $env:PORT
```

---

## Files reference

| File | Purpose |
|------|---------|
| `render.yaml` | Blueprint / IaC for Render |
| `runtime.txt` | Python version (Heroku-compatible; use with `PYTHON_VERSION` on Render) |
| `.python-version` | Render-native Python version file |
| `requirements.txt` | Pinned production dependencies |
| `requirements-dev.txt` | Dev/test/lint tools |
| `.env.example` | Documented env template |
| `scripts/render-build.sh` | Optional build script |

---

## Production checklist

- [ ] Neon database created; `DATABASE_URL` with `sslmode=require`
- [ ] Render service: root dir `backend`, correct build/start commands
- [ ] `PYTHON_VERSION=3.12.8`
- [ ] `APP_ENV=production`, `APP_DEBUG=false`
- [ ] Strong `SECRET_KEY` / `JWT_SECRET_KEY`
- [ ] `CORS_ORIGINS` set to frontend URL(s)
- [ ] Health check path `/health` returns 200
- [ ] Google OAuth redirect URIs updated for production URL
- [ ] GitHub auto-deploy tested with a small commit
