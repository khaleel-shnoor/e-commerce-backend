"""Async SQLAlchemy session manager and engine lifecycle."""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings


class DatabaseSessionManager:
    """
    Centralized async database session manager.

    Handles engine creation, session factory, and graceful shutdown.
    Inject via FastAPI dependencies — do not instantiate per request.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        connect_args: dict[str, Any] = dict(settings.database_connect_args)

        self._engine: AsyncEngine = create_async_engine(
            settings.async_database_url,
            echo=settings.app_debug,
            pool_pre_ping=True,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            connect_args=connect_args,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    async def close(self) -> None:
        """Dispose connection pool on application shutdown."""
        await self._engine.dispose()

    async def session(self) -> AsyncGenerator[AsyncSession]:
        """
        Yield a request-scoped async session.

        Commits on success, rolls back on exception.
        """
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def health_check(self) -> str:
        """Return database connectivity status for health endpoints."""
        from sqlalchemy import text

        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return "connected"
        except Exception:
            return "error"
