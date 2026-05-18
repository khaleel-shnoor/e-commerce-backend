# Day 01

## Goals

- Bootstrap the SHNOOR e-commerce backend from an empty repository
- Establish Python 3.14 project configuration and tooling
- Create scalable folder structure and documentation workflow
- Ship a minimal runnable API with health check

## Features Implemented

- Project scaffolding with `src/` layout and `shnoor` package
- `pyproject.toml` targeting Python 3.14 with FastAPI, Pydantic Settings, and dev tooling
- Centralized configuration via environment variables (`Settings`)
- FastAPI application factory with CORS and lifespan hooks
- Versioned API router (`/api/v1`)
- Health check endpoint (`GET /api/v1/health`)
- Async health endpoint test with `httpx` + `pytest-asyncio`
- Engineering journal under `docs/progress/`
- Comprehensive `README.md`

## Folder/File Changes

### New files

- `pyproject.toml` — project metadata, dependencies, Ruff, Mypy, Pytest config
- `.gitignore` — Python, venv, secrets, tooling caches
- `.env.example` — environment variable template
- `README.md` — project documentation
- `src/shnoor/__init__.py` — package version
- `src/shnoor/main.py` — FastAPI app entry point
- `src/shnoor/core/config.py` — settings management
- `src/shnoor/core/logging.py` — logging setup
- `src/shnoor/api/v1/router.py` — v1 route aggregation
- `src/shnoor/api/v1/health.py` — health endpoint
- `tests/test_health.py` — health endpoint test
- `docs/progress/template.md` — daily journal template
- `docs/progress/day-01.md` — this document

### Updated files

- N/A (greenfield project)

## API Changes

### New routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Service health, version, and UTC timestamp |

### Modified routes

- None

## Database Changes

### Collections added

- None (database layer not yet integrated)

### Schema updates

- None

## Architecture Decisions

| Decision | Why | Alternatives considered |
|----------|-----|-------------------------|
| **Python 3.14** | Latest syntax, typing, and async support for long-term maintainability | Python 3.12 LTS |
| **FastAPI** | Native async, OpenAPI docs, Pydantic v2 integration, strong ecosystem | Django REST, Starlette-only |
| **`src/` layout** | Prevents accidental imports from repo root; standard for publishable packages | Flat layout |
| **Versioned API (`/api/v1`)** | Allows non-breaking evolution as marketplace features grow | Unversioned routes |
| **Pydantic Settings** | Typed, validated config from `.env` with clear defaults | Manual `os.environ` |
| **Daily progress docs** | Onboarding, audit trail, and team continuity from day one | Ad-hoc notes only |

## Issues Faced

- Backend directory was empty; no existing conventions to extend

## Solutions

- Established conventions documented in `README.md` and this journal for all future work

## Pending Tasks

- MongoDB integration and repository layer
- Authentication (JWT) and role-based access control
- User, seller, product, order, and cart modules
- WebSocket layer for real-time notifications
- AI modules (recommendations, search, support)
- Middleware (rate limiting, request ID, error normalization)
- CI/CD pipeline

## Tomorrow Plan

- Add database connection module and base document models
- Implement authentication skeleton (register/login/refresh)
- Wire first domain route (e.g. users or categories)
- Update `day-02.md` with all changes
