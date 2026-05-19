"""FastAPI application entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from app import __version__
from app.api.v1.api import api_router
from app.api.v1.routes.health import HealthResponse, build_health_response
from app.core.config import Settings, get_settings
from app.core.database import DatabaseSessionManager
from app.core.exceptions import AppError
from app.core.logging import configure_logging
from app.core.startup import log_startup_banner, validate_settings, verify_database_on_startup
from app.db.seed import seed_roles
from app.services.oauth import configure_oauth

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: validate config, connect DB, seed roles. Shutdown: dispose engine."""
    settings: Settings = app.state.settings
    configure_logging(settings)
    log_startup_banner(settings)

    db_manager = DatabaseSessionManager(settings)
    app.state.db_manager = db_manager

    await verify_database_on_startup(db_manager, settings)
    configure_oauth(settings)

    async with db_manager._session_factory() as session:  # noqa: SLF001
        await seed_roles(session)
        await session.commit()
    logger.info("Application startup complete (version %s)", __version__)

    yield

    await db_manager.close()
    logger.info("Application shutdown complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    resolved_settings = settings or get_settings()
    validate_settings(resolved_settings)

    app = FastAPI(
        title=resolved_settings.app_name,
        version=__version__,
        description="SHNOOR intelligent e-commerce platform API — PostgreSQL, async, AI-ready.",
        docs_url="/docs" if resolved_settings.is_development else None,
        redoc_url="/redoc" if resolved_settings.is_development else None,
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings

    # Session stores OAuth state — callback must hit the same backend that started login
    app.add_middleware(
        SessionMiddleware,
        secret_key=resolved_settings.secret_key,
        same_site="lax",
        https_only=resolved_settings.is_production,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
        if resolved_settings.is_development:
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc), "type": type(exc).__name__},
            )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    @app.get("/health", include_in_schema=False, tags=["health"])
    async def root_health(request: Request) -> HealthResponse:
        """Render / load-balancer health check (no /api/v1 prefix)."""
        return await build_health_response(request)

    app.include_router(api_router)
    return app


app = create_app()


def run() -> None:
    """CLI entry point: uvicorn app.main:app --reload"""
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.is_development,
    )


if __name__ == "__main__":
    run()
