# API Structure

**Base URL:** `/api/v1`  
**OpenAPI:** `/docs` (development only)

## Route map

### System

| Method | Path | Auth |
|--------|------|------|
| GET | `/health` | No |
| GET | `/status` | No |

### Authentication (`/auth`)

| Method | Path | Auth |
|--------|------|------|
| POST | `/auth/register` | No |
| POST | `/auth/login` | No |
| POST | `/auth/refresh` | No |
| POST | `/auth/logout` | Optional Bearer |
| GET | `/auth/me` | Bearer |
| POST | `/auth/verify-email` | No |
| POST | `/auth/resend-verification` | No |
| POST | `/auth/forgot-password` | No |
| POST | `/auth/reset-password` | No |
| GET | `/auth/google/login` | No |
| GET | `/auth/google/callback` | No |

### Planned (Phase 3)

- `/products`, `/categories`, `/cart`, `/orders`
- `/seller/*`, `/admin/*`

## Request/response patterns

- Pydantic schemas in `app/schemas/`
- Errors: `{"detail": "message"}`
- Auth header: `Authorization: Bearer <access_token>`

## Frontend mapping

| Frontend route | Backend |
|----------------|---------|
| `/login` | POST `/auth/login` |
| `/register` | POST `/auth/register` |
| `/forgot-password` | POST `/auth/forgot-password` |
| `/reset-password?token=` | POST `/auth/reset-password` |
| `/auth/callback` | Google OAuth redirect |
