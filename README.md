# SHNOOR E-Commerce Backend

Scalable SaaS backend for the **SHNOOR** multi-vendor marketplace. Built with **Python 3.14**, **FastAPI**, and async-first patterns to support admin, seller, and customer flows aligned with the React frontend.

---

## Project Overview

This service powers:

- **Admin** — products, orders, sellers, coupons, CMS, analytics, support
- **Sellers** — inventory, store customization, shipping, wallet, transactions
- **Customers** — catalog, cart, checkout, reviews, notifications

The backend is designed as an enterprise-ready foundation: versioned APIs, typed configuration, modular packages, and daily engineering documentation.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                    │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP / WebSocket (future)
┌─────────────────────────────▼───────────────────────────────┐
│                    FastAPI Application                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ Middleware  │  │  API /v1     │  │  Services (future)  │ │
│  └─────────────┘  └──────────────┘  └─────────────────────┘ │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│              MongoDB (planned) · Redis · AI APIs             │
└─────────────────────────────────────────────────────────────┘
```

### Layer responsibilities

| Layer | Path | Purpose |
|-------|------|---------|
| **Entry** | `src/shnoor/main.py` | App factory, CORS, lifespan |
| **API** | `src/shnoor/api/v1/` | HTTP routes, request/response models |
| **Core** | `src/shnoor/core/` | Config, logging, security helpers |
| **Services** | `src/shnoor/services/` *(planned)* | Business logic |
| **Repositories** | `src/shnoor/repositories/` *(planned)* | Data access |
| **Models** | `src/shnoor/models/` *(planned)* | Domain & DB schemas |

---

## Setup Instructions

### Prerequisites

- [Python 3.14](https://www.python.org/downloads/)
- Git
- (Optional) MongoDB — required when the database layer is added

### Clone and enter the project

```bash
cd backend
```

---

## Python 3.14 Setup

### Windows

```powershell
# Install Python 3.14 from python.org or winget
winget install Python.Python.3.14

python --version   # should show 3.14.x
```

### macOS / Linux

```bash
pyenv install 3.14.0
pyenv local 3.14.0
python --version
```

---

## Virtual Environment Setup

```bash
# Create venv (Python 3.14)
python -m venv .venv

# Activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install project + dev dependencies
pip install -e ".[dev]"
```

### Environment variables

```bash
cp .env.example .env
# Edit .env with your local values
```

---

## Run Commands

| Command | Description |
|---------|-------------|
| `shnoor-api` | Start API server (uses `.env`) |
| `python -m shnoor.main` | Same as above |
| `uvicorn shnoor.main:app --reload` | Dev server with auto-reload |
| `pytest` | Run test suite |
| `ruff check src tests` | Lint |
| `ruff format src tests` | Format |
| `mypy src` | Type check |

### Development server

```bash
uvicorn shnoor.main:app --host 0.0.0.0 --port 8000 --reload
```

- API: http://localhost:8000  
- OpenAPI docs: http://localhost:8000/docs  
- Health: http://localhost:8000/api/v1/health  

---

## Folder Structure

```
backend/
├── docs/
│   └── progress/           # Daily engineering journal
│       ├── template.md
│       └── day-01.md
├── src/
│   └── shnoor/
│       ├── main.py         # App entry point
│       ├── api/v1/         # Versioned HTTP routes
│       └── core/           # Config, logging
├── tests/                  # Pytest suite
├── pyproject.toml          # Python 3.14 project config
├── .env.example
└── README.md
```

Planned packages (add as features land):

- `shnoor/models/` — Pydantic & DB document models  
- `shnoor/repositories/` — MongoDB access  
- `shnoor/services/` — Business logic  
- `shnoor/middleware/` — Auth, rate limits, request IDs  
- `shnoor/ai/` — Recommendations, search, support bots  
- `shnoor/websocket/` — Real-time events  

---

## Future AI Roadmap

| Phase | Capability | Integration |
|-------|------------|-------------|
| **1** | Semantic product search | Embeddings + vector store |
| **2** | Personalized recommendations | User behavior + catalog signals |
| **3** | Seller insights | Sales trends, inventory alerts |
| **4** | Support assistant | Ticket triage, FAQ, order lookup |
| **5** | Content moderation | Review & listing quality scoring |

All AI modules will live under `src/shnoor/ai/` with clear service boundaries and documented API contracts.

---

## Documentation Workflow

### Daily progress journal

Every implementation day must update `docs/progress/day-XX.md` using `docs/progress/template.md`.

**Document when you add or change:**

- Modules, routes, middleware  
- Database collections or schemas  
- Services, AI modules, auth, WebSockets  
- Architecture or optimization decisions  

### Automatic documentation rule

If you implement it, update the corresponding daily file **the same day** with:

- Goals, features, file changes  
- API and database deltas  
- Decisions, issues, solutions  
- Pending tasks and tomorrow’s plan  

---

## Coding Conventions

| Topic | Convention |
|-------|------------|
| **Python** | 3.14+, strict typing, `async` for I/O |
| **Style** | Ruff (format + lint), line length 100 |
| **Types** | Mypy strict mode; prefer `TypedDict`, `type` aliases |
| **API** | Versioned under `/api/v1`; thin routes, fat services |
| **Config** | `pydantic-settings`; never commit `.env` |
| **Errors** | Consistent HTTP exceptions; structured logging |
| **Tests** | `pytest` + `pytest-asyncio`; mirror `src/` in `tests/` |
| **Files** | Keep modules under ~300 lines; split by domain |
| **Secrets** | Environment variables only; use `.env.example` as template |

### Naming

- **Packages:** lowercase (`shnoor.services.orders`)
- **Routes:** kebab-case paths (`/api/v1/order-items`)
- **Models:** PascalCase (`ProductCreate`, `OrderDocument`)

---

## License

Proprietary — SHNOOR Engineering.
