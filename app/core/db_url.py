"""Database URL normalization for asyncpg + Neon PostgreSQL."""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

# Query params understood by libpq/Neon but not by asyncpg — strip and map to connect_args.
_STRIP_QUERY_PARAMS = frozenset(
    {
        "sslmode",
        "channel_binding",
        "options",
    }
)


def normalize_async_database_url(raw_url: str) -> tuple[str, dict[str, Any]]:
    """
    Convert a DATABASE_URL to SQLAlchemy asyncpg form and derive SSL connect_args.

    Handles:
    - postgresql:// → postgresql+asyncpg://
    - postgres:// → postgresql+asyncpg://
    - Neon sslmode=require → connect_args ssl=True
    """
    url = raw_url.strip()
    if url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url[len("postgres://") :]
    elif url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://") :]
    elif url.startswith("postgresql+asyncpg://"):
        pass
    else:
        return url, {}

    parsed = urlparse(url)
    query = parse_qs(parsed.query, keep_blank_values=True)
    ssl_required = False

    sslmode_values = query.pop("sslmode", [])
    if sslmode_values:
        mode = sslmode_values[0].lower()
        ssl_required = mode in {"require", "verify-ca", "verify-full", "prefer"}

    for key in _STRIP_QUERY_PARAMS:
        query.pop(key, None)

    new_query = urlencode({k: v[0] for k, v in query.items() if v}, doseq=False)
    clean_url = urlunparse(parsed._replace(query=new_query))

    connect_args: dict[str, Any] = {}
    if ssl_required:
        connect_args["ssl"] = True

    return clean_url, connect_args
