"""Database status endpoint — integration test (requires PostgreSQL)."""

import os

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app

requires_postgres = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS", "").lower() not in ("1", "true", "yes"),
    reason="Set RUN_DB_TESTS=1 and ensure PostgreSQL is running with migrations applied",
)


@requires_postgres
@pytest.mark.asyncio
async def test_status_reports_database_connected() -> None:
    app = create_app()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["api"] == "ok"
    assert payload["database"] == "connected"
