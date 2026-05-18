"""Health and readiness endpoints."""

from datetime import UTC, datetime
from typing import TypedDict

from fastapi import APIRouter

from shnoor import __version__

router = APIRouter(tags=["health"])


class HealthResponse(TypedDict):
    status: str
    version: str
    timestamp: str


@router.get("/health")
async def health_check() -> HealthResponse:
    """Return service health status for load balancers and monitoring."""
    return {
        "status": "ok",
        "version": __version__,
        "timestamp": datetime.now(UTC).isoformat(),
    }
