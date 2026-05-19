# Day 04 — Render + Neon Production Deployment

**Date:** 2026-05-19  
**Phase:** Infrastructure — production deploy readiness

## Completed

- [x] Analyzed FastAPI async stack, Alembic, Neon/Render compatibility
- [x] Pinned `requirements.txt` for stable GitHub auto-deploy
- [x] `requirements-dev.txt` split (dev tools not installed on Render)
- [x] `runtime.txt` + `.python-version` → Python **3.12.8** for Render
- [x] `pyproject.toml` → `requires-python >=3.12,<3.15` (local 3.14 OK)
- [x] `render.yaml` blueprint (build, start, health check, env template)
- [x] Neon `DATABASE_URL` normalization (`sslmode=require` → asyncpg SSL)
- [x] Production startup validation (`validate_settings`, DB probe logging)
- [x] `GET /health` root endpoint for Render health checks
- [x] Enhanced `/api/v1/health` with DB probe + `/health/live` liveness
- [x] JWT env aliases: `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`
- [x] CORS alias `ALLOWED_ORIGINS`; `LOG_LEVEL` support
- [x] Updated `.env.example` for production
- [x] Comprehensive `docs/deployment.md`

## Render configuration (manual dashboard)

| Setting | Value |
|---------|-------|
| Root Directory | `backend` |
| Build Command | `pip install --upgrade pip && pip install -r requirements.txt && alembic upgrade head` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |
| PYTHON_VERSION | `3.12.8` |

## Decisions

- **Python 3.12.8 on Render** — stability over 3.14 for native wheels (asyncpg, cryptography)
- **pip only** — no Poetry on Render; `requirements.txt` is source of truth for deploy
- **uvicorn ASGI** — not gunicorn WSGI (FastAPI is async)
- **Migrations in build step** — `alembic upgrade head` before each deploy
- **Fail-fast production config** — weak secrets / missing `DATABASE_URL` exit at startup

## Next

- [ ] First successful Render deploy + Neon connection verified
- [ ] Set production `CORS_ORIGINS` and Google OAuth redirect URIs
- [ ] Frontend `VITE_API_URL` pointing to Render backend URL
- [ ] Optional: gunicorn + UvicornWorker for multi-worker scaling
