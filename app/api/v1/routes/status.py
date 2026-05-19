"""Extended status endpoint — includes database connectivity probe."""

from typing import TypedDict

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DbSession

router = APIRouter(tags=["status"])


class StatusResponse(TypedDict):
    api: str
    database: str


@router.get("/status", summary="API and database status")
async def system_status(db: DbSession) -> StatusResponse:
    """
    Verify API is running and PostgreSQL is reachable.

    Does not expose sensitive configuration.
    """
    db_status = "disconnected"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return {"api": "ok", "database": db_status}
