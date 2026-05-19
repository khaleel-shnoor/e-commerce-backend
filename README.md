# SHNOOR E-Commerce Backend

Production-grade, **async-first**, **AI-ready** SaaS API for the SHNOOR multi-vendor marketplace. Built with **Python 3.14**, **FastAPI**, and **PostgreSQL** (SQLAlchemy 2.0 async + Alembic).

---

## Project Overview

Powers admin, seller, and customer experiences for the React frontend:

- Catalog, cart, orders, reviews, coupons
- Seller stores, inventory, transactions
- Admin moderation, analytics, notifications
- **Future:** semantic search, recommendations, AI agents (pgvector)

---

## Architecture Overview

```
React Frontend
      │
      ▼
FastAPI (app/main.py)
      ├── API v1 routes
      ├── Services (business logic)
      ├── Repositories (data access)
      └── SQLAlchemy async ──► PostgreSQL
                ▲
           Alembic migrations
```

**AI modules** live under `app/ai/` (recommendations, embeddings, search, ranking, agents, personalization).

Full system context: [`docs/project-context.md`](docs/project-context.md)

---

## Python 3.14 Setup

```powershell
# Windows
winget install Python.Python.3.14
python --version   # 3.14.x
```

```bash
# macOS / Linux
pyenv install 3.14.0 && pyenv local 3.14.0
```

---

## Virtual Environment

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
# or: pip install -r requirements.txt
```

---

## PostgreSQL Setup

### 1. Install PostgreSQL 16+

Ensure the server is running locally or use Docker:

```powershell
docker run -d --name shnoor-postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=shnoor `
  -p 5432:5432 postgres:16
```

### 2. Create database

```sql
CREATE DATABASE shnoor;
```

### 3. Configure environment

```powershell
copy .env.example .env
# Edit DATABASE_URL if needed:
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/shnoor
```

---

## Alembic Migration Setup

```powershell
# Generate initial migration from models
alembic revision --autogenerate -m "initial_schema"

# Review alembic/versions/*.py, then apply:
alembic upgrade head

# Or use helper script:
.\scripts\migrate.ps1 "initial_schema"
.\scripts\migrate.ps1 upgrade
```

---

## Run Commands

| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | **Primary** dev server |
| `shnoor-api` | Same via CLI entry point |
| `alembic upgrade head` | Apply migrations |
| `pytest` | Unit tests |
| `RUN_DB_TESTS=1 pytest` | Include PostgreSQL integration tests |
| `black app tests` | Format |
| `isort app tests` | Sort imports |
| `pylint app` | Lint |

### URLs (development)

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Health: http://localhost:8000/api/v1/health  
- Status: http://localhost:8000/api/v1/status  

---

## Folder Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/v1/          # Routes
│   ├── core/            # Config, DB, security, deps
│   ├── models/          # SQLAlchemy ORM (20 tables)
│   ├── schemas/         # Pydantic DTOs
│   ├── repositories/    # Data access
│   ├── services/        # Business logic
│   ├── ai/              # AI subsystems (placeholders)
│   ├── admin|seller|customer/
│   ├── jobs|websockets|events|middleware/
├── alembic/             # Migrations
├── tests/
├── docs/
│   ├── project-context.md   # Master AI handoff doc
│   └── progress/            # Daily engineering logs
├── scripts/
├── uploads/  logs/
├── pyproject.toml
└── requirements.txt
```

---

## Documentation Workflow

### 1. Daily engineering logs

`docs/progress/day-XX.md` — copy from `template.md` each day.

Document: goals, features, files, DB changes, routes, decisions, issues, tomorrow plan.

### 2. Master project context

**Always update** [`docs/project-context.md`](docs/project-context.md) when you add:

- Routes, models, auth, AI modules, WebSockets, middleware, architecture changes

This file is the **single source of truth** for AI tools and new developers.

---

## AI Roadmap

| Phase | Capability |
|-------|------------|
| 4 | pgvector embeddings, semantic search |
| 4 | Recommendation engine |
| 5 | AI agents / chatbots |
| 5 | Personalization, ranking ML |

Code placeholders: `app/ai/*`

---

## Project Scaling Vision

- **Phase 1:** Foundation (current) — PostgreSQL, models, health API  
- **Phase 2:** Auth, CRUD, admin/seller/customer APIs  
- **Phase 3:** Redis cache, Celery jobs, WebSockets, events  
- **Phase 4:** pgvector, semantic search, recommendations  
- **Phase 5:** AI agents, analytics ML, multi-region  

Designed for horizontal API scaling, read replicas, and event-driven order processing.

---

## Coding Conventions

- Async routes and repositories  
- Thin routes → services → repositories  
- UUID PKs, typed enums, timezone timestamps  
- black + isort + pylint  
- Update `docs/project-context.md` + daily log with every significant change  

---

## License

Proprietary — SHNOOR Engineering.
