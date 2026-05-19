# SHNOOR E-Commerce Backend — Master Project Context

> **AI handoff document.** Provide this file alone to understand architecture, progress, patterns, and roadmap.
> **Last updated:** Day 03 — Authentication + extended schema

---

## Project Overview

**SHNOOR** is a multi-vendor intelligent e-commerce SaaS platform. The React frontend (`../frontend`) provides admin, seller, and customer UIs with placeholder data. This backend will power all APIs with a production-grade, async-first, AI-ready foundation.

**Current phase:** Auth + Schema (v0.3.0) — Full auth system, extended DB (~45 tables), frontend integration. Domain CRUD APIs pending Phase 3.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.14 |
| API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 (async) |
| Driver | asyncpg |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth (planned) | JWT + passlib[bcrypt] |
| Config | pydantic-settings + python-dotenv |
| Server | uvicorn |
| Dev tools | black, isort, pylint, pytest |

**Future:** Redis, Celery/RQ, pgvector, WebSockets, event bus

---

## Architecture Overview

```
Client (React) → FastAPI (app/main.py)
                    ├── Middleware (Phase 2+)
                    ├── API v1 routes (thin)
                    ├── Services (business logic)
                    ├── Repositories (data access)
                    └── SQLAlchemy async → PostgreSQL
                              ↑
                    Alembic migrations
```

**AI subsystem** (`app/ai/`) sits alongside services, calling repositories and external model APIs. Embeddings stored in PostgreSQL via pgvector (Phase 4).

---

## Folder Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry — uvicorn app.main:app
│   ├── api/v1/
│   │   ├── api.py           # Router aggregation
│   │   └── routes/          # health, status, (future: auth, products…)
│   ├── core/
│   │   ├── config.py        # Settings
│   │   ├── database.py      # DatabaseSessionManager
│   │   ├── dependencies.py  # get_db_session, DbSession
│   │   ├── security.py      # JWT + bcrypt (stubs)
│   │   ├── constants.py
│   │   └── logging.py
│   ├── models/              # SQLAlchemy ORM (20 tables)
│   ├── schemas/             # Pydantic DTOs (minimal)
│   ├── repositories/        # BaseRepository + domain repos
│   ├── services/            # Business logic (Phase 2)
│   ├── middleware/          # Phase 2+
│   ├── validators/
│   ├── utils/
│   ├── ai/                  # recommendations, embeddings, search, ranking, agents, personalization
│   ├── jobs/                # Celery/RQ
│   ├── websockets/
│   ├── events/
│   ├── admin/, seller/, customer/
├── alembic/
├── tests/
├── docs/
│   ├── project-context.md   # THIS FILE
│   └── progress/day-XX.md
├── scripts/
├── uploads/, logs/
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Coding Standards

- Python 3.14, strict typing, async I/O in routes and repositories
- Line length 100; format with **black**, sort imports with **isort**
- Routes thin; logic in **services**; DB access in **repositories**
- UUID primary keys; timezone-aware timestamps
- Versioned API: `/api/v1`
- Never commit `.env`; use `.env.example`
- Update **this file** and **daily progress log** when adding features

---

## Database Design

**Engine:** PostgreSQL via `postgresql+asyncpg://`

**Session management:** `DatabaseSessionManager` in `app/core/database.py` — one engine per app, sessions per request via `get_db_session`.

### Entity relationship summary

- **users** ↔ **roles** (M2M `user_roles`)
- **users** → **sellers** | **admins** (1:1 profile)
- **sellers** → **products** → **product_images**, **inventory**
- **categories** (self-referential parent) → **products**
- **users** → **carts** → **cart_items** → **products**
- **users** → **wishlists** → **products**
- **users** → **orders** → **order_items** → **products**
- **users** → **addresses**, **reviews**, **notifications**
- **orders** → **transactions**
- **coupons** — standalone promo codes

### Enums (`app/models/enums.py`)

`RoleName`, `SellerStatus`, `ProductStatus`, `OrderStatus`, `CouponDiscountType`, `NotificationType`, `TransactionType`, `TransactionStatus`, `AddressType`

### Future AI tables

`app/models/ai_embeddings.py` — documented placeholder for pgvector `product_embeddings` (Phase 4).

---

## API Architecture

- Prefix: `/api/v1` (`app/core/constants.py`)
- Router aggregation: `app/api/v1/api.py`
- OpenAPI at `/docs` (development only)

---

## Authentication Flow (Implemented — v0.3.0)

**Methods:** Email/password, Google OAuth, forgot password, email verification.

**Token lifecycle:**

1. Login/register/OAuth → access JWT (30m) + refresh JWT (7d, `jti` → `refresh_tokens` row)
2. Refresh → rotate: revoke old row, issue new pair
3. Logout → revoke refresh token row

**Routes:** `app/api/v1/routes/auth.py` — see `docs/api-structure.md`

**Dependencies:** `CurrentUser`, `require_roles()`, `AuthServiceDep`

**OAuth:** Authlib Google; callback redirects to `{FRONTEND_URL}/auth/callback?access_token=...`

**Security:** bcrypt passwords; reset/verify tokens SHA-256 hashed; no email enumeration on forgot-password

---

## Roles & Permissions

| Role | Access |
|------|--------|
| admin | Full platform moderation, analytics, CMS |
| seller | Own products, orders, wallet, store |
| customer | Browse, cart, checkout, reviews |

Stored in `roles` table; assigned via `user_roles`.

---

## Service Layer Design

- One service class per domain aggregate (e.g. `ProductService`)
- Accepts `AsyncSession` or repositories via constructor
- Raises domain exceptions; routes map to HTTP status
- No raw SQL in routes

---

## Repository Layer Design

- `BaseRepository[ModelT]` — `get_by_id`, `list_all`, `add`, `delete`
- Domain repos extend base with filtered queries
- All methods `async`

---

## AI Architecture Plan

| Package | Purpose |
|---------|---------|
| `app/ai/recommendations` | Collaborative + content-based suggestions |
| `app/ai/embeddings` | Vector generation and pgvector storage |
| `app/ai/search` | Semantic + hybrid search |
| `app/ai/ranking` | Re-ranking with business rules |
| `app/ai/agents` | LLM chatbots with tools |
| `app/ai/personalization` | User preference models |

**Data flow (future):** Product change → job embeds → pgvector → search/recommendation APIs

---

## Current Implemented Features

- [x] FastAPI app with lifespan, CORS, SessionMiddleware
- [x] Async PostgreSQL session manager
- [x] ~45 ORM models (commerce + auth + extensions + AI-ready)
- [x] Alembic migrations 001 + 002
- [x] Health and DB status endpoints
- [x] Full authentication API (JWT, OAuth, reset, verify)
- [x] AuthService, OAuthService, EmailService
- [x] User/auth repositories
- [x] RBAC dependencies
- [x] AI folder placeholders
- [x] Documentation system

---

## Pending Features

- [ ] Domain CRUD routes (products, cart, orders, seller, admin)
- [ ] Redis caching
- [ ] Celery jobs
- [ ] WebSockets
- [ ] pgvector + embeddings
- [ ] Payment gateway integration
- [ ] Full test coverage

---

## API Endpoints Summary

| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/api/v1/health` | No | Live |
| GET | `/api/v1/status` | No | Live (DB probe) |
| POST | `/api/v1/auth/*` | Mixed | Live — see api-structure.md |
| GET | `/api/v1/auth/google/*` | No | Live (if Google env set) |

---

## Database Tables Summary

| Table | PK | Key FKs |
|-------|-----|---------|
| users | UUID | — |
| roles | UUID | — |
| user_roles | composite | users, roles |
| sellers | UUID | users |
| admins | UUID | users |
| categories | UUID | categories (parent) |
| products | UUID | sellers, categories |
| product_images | UUID | products |
| carts | UUID | users |
| cart_items | UUID | carts, products |
| wishlists | UUID | users, products |
| orders | UUID | users, addresses |
| order_items | UUID | orders, products |
| reviews | UUID | users, products |
| inventory | UUID | products |
| addresses | UUID | users |
| coupons | UUID | — |
| notifications | UUID | users |
| transactions | UUID | orders |

---

## Important Decisions

1. **PostgreSQL over MongoDB** — relational model, ACID, pgvector for AI
2. **`app/` not `src/shnoor/`** — aligns with spec and `uvicorn app.main:app`
3. **No auth routes in foundation** — avoid half-implemented security
4. **UUID everywhere** — scale-friendly IDs
5. **Dual documentation** — daily logs + this master file

---

## Reusable Patterns

```python
# DB dependency in route
@router.get("/example")
async def example(db: DbSession):
    ...

# Repository usage
repo = UserRepository(db)
user = await repo.get_by_id(user_id)

# Settings
settings = get_settings()
url = settings.async_database_url
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| APP_NAME, APP_ENV, APP_DEBUG, APP_HOST, APP_PORT | Application |
| DATABASE_URL | Full async PostgreSQL URL (preferred) |
| POSTGRES_* | Composed URL if DATABASE_URL empty |
| SECRET_KEY, ALGORITHM | JWT |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token TTL |
| CORS_ORIGINS | Comma-separated origins |
| SMTP_ENABLED | Enable outbound email |
| SMTP_HOST, SMTP_PORT, SMTP_SECURE | Gmail: `smtp.gmail.com`, `587`, `false` (STARTTLS) |
| SMTP_USER, SMTP_FROM, SMTP_PASS | Sender credentials (Gmail App Password) |

See `.env.example`.

**Email service:** `app/services/email/` — `EmailService.send_email()` for all outbound mail; helpers for password reset, verification, and `send_order_placed()` (future).

---

## Deployment Plan

**Target:** [Render](https://render.com) (web service) + [Neon](https://neon.tech) (PostgreSQL)

| Step | Action |
|------|--------|
| 1 | Create Neon project; copy `DATABASE_URL` with `?sslmode=require` |
| 2 | Create Render web service — **Root Directory:** `backend` |
| 3 | **Build:** `pip install --upgrade pip && pip install -r requirements.txt && alembic upgrade head` |
| 4 | **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| 5 | **Health check:** `/health` |
| 6 | Set production env vars (`APP_ENV=production`, secrets, `CORS_ORIGINS`) |
| 7 | Enable GitHub auto-deploy on `main` |

**Python version:** Deploy on **3.12.8** (Render). Local **3.14** supported via `requires-python >=3.12,<3.15`.

**Full guide:** [`docs/deployment.md`](deployment.md)

**Artifacts:** `render.yaml`, `runtime.txt`, `.python-version`, pinned `requirements.txt`

---

## Scaling Strategy

- **API:** Stateless replicas behind load balancer
- **DB:** Read replicas, indexing, query optimization
- **Cache:** Redis for sessions, catalog, rate limits
- **Jobs:** Celery workers for embeddings, emails, reports
- **Events:** Redis streams or Kafka for order pipeline
- **AI:** Dedicated workers + vector index in PostgreSQL

---

## Future Roadmap

| Phase | Focus |
|-------|-------|
| 1 | Foundation (current) |
| 2 | Auth + core CRUD |
| 3 | Cart, checkout, WebSockets |
| 4 | pgvector, semantic search, recommendations |
| 5 | AI agents, analytics ML |
| 6 | Multi-region, advanced scaling |

---

## Known Issues

- Initial Alembic migration must be generated/applied per environment
- `/api/v1/status` returns `database: error` if PostgreSQL is down (expected)
- bcrypt/passlib may warn on Python 3.14 — monitor library updates

---

## Implementation Timeline

| Day | Milestone |
|-----|-----------|
| 01 | FastAPI bootstrap (MongoDB mentioned — superseded) |
| 02 | PostgreSQL architecture, models, Alembic, AI structure |
| 03 | Auth system, extended schema, frontend integration |
| 04+ | Domain APIs, Redis, Celery |

---

## Documentation Workflow

1. **Daily:** `docs/progress/day-XX.md` from template
2. **Master:** Update this file on any architecture/API/DB change
3. **README:** User-facing setup and conventions
