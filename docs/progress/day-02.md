# Day 02

## Goals

- Replace MongoDB architecture with PostgreSQL entirely
- Implement SQLAlchemy 2.0 async + asyncpg + Alembic
- Restructure project to `app/` layout per enterprise spec
- Create starter ORM models for all core commerce entities
- Establish AI-ready folder structure and master project context doc

## Features Implemented

- Full migration from `src/shnoor/` to `app/` package layout
- `DatabaseSessionManager` with async session lifecycle and FastAPI DI
- Pydantic Settings with `DATABASE_URL` and composed PostgreSQL URL
- 20 starter tables with UUID PKs, FKs, enums, timestamps, indexes
- `BaseRepository` generic async repository pattern
- JWT/password security primitives (not wired to routes — Phase 2)
- Alembic async migration environment
- Health + database status API routes
- AI subsystem placeholders (`app/ai/*`)
- Master `docs/project-context.md` for AI handoff
- Updated README with PostgreSQL and Alembic instructions

## Files Added

- `app/` — full application package (core, models, api, repositories, schemas, ai, …)
- `alembic/` — migration environment
- `alembic.ini`
- `requirements.txt`
- `scripts/migrate.ps1`, `scripts/migrate.sh`
- `app/models/*` — all ORM models
- `docs/project-context.md`
- `docs/progress/day-02.md`
- `tests/conftest.py`, `tests/test_status.py`
- `logs/.gitkeep`, `uploads/.gitkeep`

## Files Modified

- `pyproject.toml` — PostgreSQL stack, black/isort/pylint, `app` package
- `.env.example` — PostgreSQL vars (removed MongoDB)
- `.gitignore`
- `README.md` — full rewrite
- `docs/progress/template.md` — updated sections
- `tests/test_health.py`

## Files Removed

- `src/shnoor/` — entire legacy package

## Database Changes

### Tables added (via models — run `alembic revision --autogenerate`)

| Table | Purpose |
|-------|---------|
| users | Platform accounts |
| roles, user_roles | RBAC |
| sellers, admins | Role profiles |
| categories | Product taxonomy |
| products, product_images | Catalog |
| carts, cart_items, wishlists | Shopping |
| orders, order_items | Checkout |
| reviews | Product feedback |
| inventory | Stock |
| addresses | Shipping/billing |
| coupons | Promotions |
| notifications | Alerts |
| transactions | Payments (schema only) |

### Migrations

- Alembic env configured; initial migration generated via `alembic revision --autogenerate -m "initial_schema"`

## Routes Added

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Service health |
| GET | `/api/v1/status` | API + PostgreSQL connectivity |

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| PostgreSQL over MongoDB | Relational integrity, joins, ACID, pgvector for AI |
| SQLAlchemy 2.0 async | Native async with FastAPI; mature ecosystem |
| Repository pattern | Testable data layer; thin routes |
| UUID primary keys | Distributed-friendly, no sequential leaks |
| `app/` flat layout | Matches spec; `uvicorn app.main:app` |
| Security stubs only | Foundation before auth routes |
| AI as subpackages | Clear boundaries for recommendations, search, agents |

## Problems Faced

- Greenfield restructure from Day 01 MongoDB references

## Solutions

- Complete replacement documented in `project-context.md` and README

## Pending Work

- Run and verify Alembic initial migration against local PostgreSQL
- JWT auth routes and role guards
- Domain services and Pydantic schemas per module
- Redis, Celery, pgvector extension
- WebSocket notifications
- Seed scripts for roles and admin user

## Tomorrow Plan

- Apply initial migration; add DB seed script
- Implement auth register/login skeleton
- First CRUD module (categories or products)
- Update `day-03.md` and `project-context.md`
