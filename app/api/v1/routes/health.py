"""Health and readiness endpoints."""

from datetime import UTC, datetime
from typing import TypedDict

from fastapi import APIRouter, Request

from app import __version__

router = APIRouter(tags=["health"])


class HealthResponse(TypedDict):
    status: str
    version: str
    timestamp: str
    database: str


async def build_health_response(request: Request | None = None) -> HealthResponse:
    """
    Build health payload with optional database probe.

    Used by /api/v1/health and root /health (Render health checks).
    """
    db_status = "unknown"
    if request is not None and hasattr(request.app.state, "db_manager"):
        db_manager = request.app.state.db_manager
        db_status = await db_manager.health_check()

    overall_status = "ok" if db_status in {"connected", "unknown"} else "degraded"

    return {
        "status": overall_status,
        "version": __version__,
        "timestamp": datetime.now(UTC).isoformat(),
        "database": db_status,
    }


@router.get("/health", summary="Service health check")
async def health_check(request: Request) -> HealthResponse:
    """
    Return service health for load balancers and monitoring.

    Probes PostgreSQL when the app has finished startup.
    """
    return await build_health_response(request)


@router.get("/health/live", summary="Liveness probe (no database)")
async def liveness_check() -> HealthResponse:
    """Fast liveness check — API process only, no DB round-trip."""
    return {
        "status": "ok",
        "version": __version__,
        "timestamp": datetime.now(UTC).isoformat(),
        "database": "not_checked",
    }
