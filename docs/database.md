# Database Schema Reference

## Connection

- URL: `DATABASE_URL` or composed `POSTGRES_*` vars
- Driver: `postgresql+asyncpg://`
- Pool: size 10, overflow 20, pre-ping

## Migrations

```bash
alembic upgrade head
alembic revision --autogenerate -m "description"
```

| Revision | Description |
|----------|-------------|
| `20260518_001` | Foundation commerce (19 tables) |
| `20260518_002` | Auth + extended schema |

## Entity groups

See `docs/project-context.md` (monorepo root) for full table list.

### Auth tables

- **users** — `password_hash` nullable for OAuth-only accounts
- **refresh_tokens** — hashed opaque storage, revocation, expiry
- **oauth_accounts** — provider + provider_user_id unique
- **password_reset_tokens** — one-time, hashed
- **email_verification_tokens** — one-time, hashed

### Wishlist normalization

- `wishlists` — one per user (unique `user_id`)
- `wishlist_items` — product lines

### Soft delete

`SoftDeleteMixin` on: `brands`, `product_variants`, and extensible to products/orders in Phase 3.

## Indexing strategy

- All FK columns indexed
- Unique: email, slugs, oauth provider pairs, coupon codes
- Status/enums indexed for filter queries

## AI-ready tables

`embeddings`, `recommendation_scores`, `search_analytics`, `personalization_data` — populated in Phase 4; `vector_data` TEXT until pgvector migration.
