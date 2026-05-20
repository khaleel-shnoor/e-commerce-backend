"""URL slug helpers."""

import re
import uuid


def slugify(value: str) -> str:
    """Convert a store name (or slug input) to a URL-safe slug."""
    slug = value.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-") or "store"


async def unique_store_slug(_session, base_slug: str, *, exists) -> str:
    """Return base_slug or base_slug-N if taken."""
    candidate = base_slug
    suffix = 1
    while await exists(candidate):
        candidate = f"{base_slug}-{suffix}"
        suffix += 1
        if suffix > 100:
            candidate = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            break
    return candidate
