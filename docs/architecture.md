# Backend Architecture

## Layered design

```
HTTP Request
    ↓
FastAPI Router (app/api/v1/routes/)
    ↓
Dependencies (app/core/dependencies.py)
    ↓
Service (app/services/) — business rules, orchestration
    ↓
Repository (app/repositories/) — queries, persistence
    ↓
SQLAlchemy AsyncSession
    ↓
PostgreSQL
```

## Application lifecycle

1. `create_app()` — settings on `app.state`, CORS, SessionMiddleware (OAuth)
2. Lifespan — `DatabaseSessionManager`, OAuth config, role seeding
3. Per-request — `get_db_session` commits/rollbacks automatically

## Error handling

Domain errors inherit `AppError` with `status_code`. Global handler returns `{"detail": message}`.

## Auth dependencies

- `CurrentUser` — Bearer JWT, loads user + roles
- `require_roles(RoleName.ADMIN, ...)` — RBAC factory
- `AuthServiceDep` — injects `AuthService`

## Extension points

- `app/middleware/` — rate limiting, request ID (Phase 3)
- `app/events/` — domain events (Phase 3)
- `app/jobs/` — Celery tasks (Phase 3)
- `app/ai/` — ML/vector pipelines (Phase 4+)
