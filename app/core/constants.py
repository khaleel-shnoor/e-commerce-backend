"""Application-wide constants."""

API_V1_PREFIX = "/api/v1"

# Role identifiers (match Role.name in database seeds)
ROLE_ADMIN = "admin"
ROLE_SELLER = "seller"
ROLE_CUSTOMER = "customer"

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# AI / search (future)
DEFAULT_EMBEDDING_DIMENSION = 1536
SEMANTIC_SEARCH_TOP_K = 20
