"""Production startup validation and diagnostic logging."""

from __future__ import annotations

import logging
import sys

from sqlalchemy import text

from app.core.config import Settings
from app.core.database import DatabaseSessionManager

logger = logging.getLogger(__name__)

_INSECURE_SECRETS = frozenset(
    {
        "change-me-in-production",
        "change-me-in-production-use-openssl-rand-hex-32",
    }
)


def validate_settings(settings: Settings) -> None:
    """
    Fail fast when production configuration is unsafe or incomplete.

    Skipped for development/test to keep local and pytest flows simple.
    """
    if settings.app_env != "production":
        return

    errors: list[str] = []

    if not settings.database_url:
        errors.append("DATABASE_URL is required when APP_ENV=production")

    if settings.secret_key in _INSECURE_SECRETS or len(settings.secret_key) < 32:
        errors.append(
            "SECRET_KEY must be a strong random value (32+ characters). "
            "Generate with: openssl rand -hex 32"
        )

    # Optional overrides — only validate when explicitly set (otherwise SECRET_KEY is used)
    if settings.jwt_secret_key is not None:
        if settings.jwt_secret_key in _INSECURE_SECRETS or len(settings.jwt_secret_key) < 32:
            errors.append("JWT_SECRET_KEY must be a strong random value when set in production")

    if settings.jwt_refresh_secret_key is not None:
        if (
            settings.jwt_refresh_secret_key in _INSECURE_SECRETS
            or len(settings.jwt_refresh_secret_key) < 32
        ):
            errors.append(
                "JWT_REFRESH_SECRET_KEY must be a strong random value when set in production"
            )

    if settings.app_debug:
        errors.append("APP_DEBUG must be false in production")

    if "*" in settings.cors_origins:
        errors.append("CORS_ORIGINS must not include '*' when allow_credentials=True")

    if not settings.cors_origins:
        errors.append("CORS_ORIGINS must include your frontend URL in production")

    if errors:
        for message in errors:
            logger.error("Startup configuration error: %s", message)
        sys.exit(1)


def log_startup_banner(settings: Settings) -> None:
    """Emit a concise, secret-safe startup summary for Render logs."""
    db_target = "configured" if settings.database_url else "composed from POSTGRES_*"
    logger.info(
        "Starting %s | env=%s | debug=%s | database=%s | cors_origins=%d",
        settings.app_name,
        settings.app_env,
        settings.app_debug,
        db_target,
        len(settings.cors_origins),
    )


async def verify_database_on_startup(
    db_manager: DatabaseSessionManager,
    settings: Settings,
) -> None:
    """Probe PostgreSQL once at startup; surfaces Neon/SSL issues early in logs."""
    try:
        async with db_manager.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection verified successfully")
    except Exception:
        logger.exception("Database connection failed during startup")
        if settings.is_production:
            raise
