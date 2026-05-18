"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shnoor import __version__
from shnoor.api.v1.router import api_router
from shnoor.core.config import Settings, get_settings
from shnoor.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage startup and shutdown lifecycle hooks."""
    settings: Settings = app.state.settings
    configure_logging(settings)
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    resolved_settings = settings or get_settings()

    app = FastAPI(
        title=resolved_settings.app_name,
        version=__version__,
        docs_url="/docs" if resolved_settings.is_development else None,
        redoc_url="/redoc" if resolved_settings.is_development else None,
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()


def run() -> None:
    """Run the API server via CLI entry point."""
    settings = get_settings()
    uvicorn.run(
        "shnoor.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.is_development,
    )


if __name__ == "__main__":
    run()
