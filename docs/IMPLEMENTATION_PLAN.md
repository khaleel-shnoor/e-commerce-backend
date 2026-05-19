# SHNOOR — Auth & Database Implementation Plan

> **Status:** Approved architecture for Phase 2 (Auth + Extended Schema)  
> **Prerequisite:** Foundation v0.2.0 (19 commerce tables, health/status routes)

---

## Phase 1 — System Analysis Summary

### Frontend (React + Tailwind v4)

| Area | Count | State |
|------|-------|-------|
| Public routes | 10 | Mock data from `src/data/` |
| Auth routes | 5 | UI only — no API |
| Customer dashboard | 14 | Mix of mock + placeholders |
| Seller dashboard | 16 | Mostly placeholders |
| Admin dashboard | 16 | Mostly placeholders |

**Auth gaps:** No JWT, no OAuth, no persistence, forgot→OTP chain broken, `logout` unused, Navbar always shows login.

### Backend (FastAPI + PostgreSQL)

| Layer | State |
|-------|-------|
| ORM models | 19 tables — commerce core |
| Routes | `/health`, `/status` only |
| Services | None |
| Domain repos | `BaseRepository` only |
| Security | JWT + bcrypt primitives |
| Auth routes | Not implemented |

---

## Phase 2 — Database Architecture Decisions

### Design principles

1. **UUID PKs** — all new tables use `UUIDPrimaryKeyMixin`
2. **Timestamps** — `TimestampMixin` on all entities
3. **Soft delete** — `SoftDeleteMixin` on user-facing catalog/order entities (Phase 2b)
4. **OAuth users** — `users.password_hash` becomes **nullable**
5. **Refresh tokens** — stored **hashed** (SHA-256); rotation on refresh
6. **Reset/verify tokens** — stored **hashed**; single-use; expiry enforced
7. **Wishlist normalization** — `wishlists` (header) + `wishlist_items` (lines)
8. **Incremental migrations** — `20260518_002_auth_and_extensions.py` after initial schema

### New tables (this implementation)

#### AUTH (required now)

| Table | Purpose |
|-------|---------|
| `refresh_tokens` | Rotating refresh token sessions |
| `oauth_accounts` | Google (extensible) provider linkage |
| `password_reset_tokens` | Forgot-password one-time tokens |
| `email_verification_tokens` | Email confirm flow |
| `user_sessions` | Optional session audit trail |

#### COMMERCE EXTENSIONS (schema-ready)

| Table | Purpose |
|-------|---------|
| `brands` | Product brand master |
| `product_variants` | SKU variants (size/color) |
| `product_categories` | M2M product ↔ category |
| `wishlist_items` | Normalized wishlist lines |
| `payments` | Order payment records |
| `coupon_usages` | Per-user coupon redemption |
| `review_images` | Review media |
| `returns` | Return requests |

#### SELLER / ADMIN / SYSTEM / AI (schema-ready)

| Group | Tables |
|-------|--------|
| Seller | `seller_documents`, `seller_payouts`, `seller_wallets`, `seller_settings` |
| Admin | `admin_logs`, `reports`, `support_tickets`, `banners`, `cms_pages` |
| System | `notification_preferences`, `audit_logs`, `activity_logs` |
| AI-ready | `embeddings`, `recommendation_scores`, `search_analytics`, `personalization_data` |

> Full commerce API routes remain Phase 3+. This phase delivers **auth + schema foundation**.

---

## Phase 3 — Authentication Architecture

### Token lifecycle

```
Register/Login/OAuth
    → access JWT (30m, HS256, sub=user_id, roles[])
    → refresh token (7d, opaque, stored hashed in DB)

Refresh
    → validate refresh token hash + expiry + not revoked
    → revoke old refresh token (rotation)
    → issue new access + refresh pair

Logout
    → revoke refresh token(s) for session
```

### Endpoints

| Method | Path | Auth |
|--------|------|------|
| POST | `/api/v1/auth/register` | Public |
| POST | `/api/v1/auth/login` | Public |
| POST | `/api/v1/auth/refresh` | Public (refresh body) |
| POST | `/api/v1/auth/logout` | Bearer |
| GET | `/api/v1/auth/me` | Bearer |
| POST | `/api/v1/auth/verify-email` | Public |
| POST | `/api/v1/auth/resend-verification` | Public |
| GET | `/api/v1/auth/google/login` | Public |
| GET | `/api/v1/auth/google/callback` | Public |
| POST | `/api/v1/auth/forgot-password` | Public |
| POST | `/api/v1/auth/reset-password` | Public |

### Google OAuth merge strategy

1. If `oauth_accounts` exists for Google `sub` → login that user
2. If email exists (password account) → link OAuth to existing user (no duplicate)
3. Else → create user + customer role + oauth_account

### Forgot password

1. `POST /forgot-password` — always 200 (no email enumeration)
2. Generate 32-byte url-safe token → store SHA-256 hash, 1h expiry
3. Dev: log token to console; Prod: send email (stub `EmailService`)
4. `POST /reset-password` — validate token, update password, mark token used

### RBAC

- Roles seeded: `admin`, `seller`, `customer`
- JWT includes `roles: string[]`
- `require_roles(*roles)` dependency for protected routes

---

## Phase 4 — Backend File Layout

```
app/
├── models/auth.py, commerce_ext.py, seller_ext.py, admin_ext.py, system_ext.py, ai_ext.py
├── schemas/auth.py
├── repositories/user.py, auth.py
├── services/auth.py, email.py, oauth.py
├── api/v1/routes/auth.py
├── core/dependencies.py  (+ get_current_user, require_roles)
├── core/security.py        (+ refresh tokens, token hashing)
└── db/seed.py              (role seeding)
```

---

## Phase 5 — Frontend Integration

```
frontend/src/
├── lib/api.js           # fetch wrapper + auth header
├── lib/auth-storage.js  # localStorage tokens
├── context/AuthContext.jsx  # real API login/logout/refresh
├── pages/auth/*.jsx     # wire forms + Google button
└── routes/ProtectedRoute.jsx  # token + role guard
```

Environment: `VITE_API_URL=http://localhost:8000`

---

## Phase 6 — Documentation Deliverables

| File | Action |
|------|--------|
| `backend/docs/project-context.md` | Full rewrite — auth, DB, OAuth |
| `backend/docs/architecture.md` | Create |
| `backend/docs/database.md` | Create |
| `backend/docs/api-structure.md` | Create |
| `backend/docs/progress/day-03.md` | Create |
| `docs/project-context.md` | Master monorepo context |
| `frontend/src/docs/auth-flow.md` | Create |
| `frontend/src/docs/routing.md` | Update |

---

## Security Checklist

- [x] bcrypt passwords
- [x] JWT access tokens with expiry
- [x] Refresh token rotation + DB storage (hashed)
- [x] Reset tokens hashed + one-time + expiry
- [x] OAuth state parameter (Authlib)
- [x] No secrets in code — `.env` only
- [x] CORS with credentials for future cookies
- [ ] Rate limiting (Phase 3)
- [ ] HttpOnly cookies (prepared, using Bearer for SPA now)

---

## Implementation Order

1. Models + enums + migration
2. Security helpers + seed roles
3. Repositories + services
4. Auth routes + dependencies
5. Tests (auth happy path)
6. Frontend integration
7. Documentation
