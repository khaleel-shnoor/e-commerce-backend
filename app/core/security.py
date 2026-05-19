"""Security utilities — JWT, password hashing, and opaque token hashing."""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import bcrypt
from jose import JWTError, jwt

from app.core.config import Settings


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password for storage (bcrypt)."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    """Verify a plaintext password against a stored hash."""
    if not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except ValueError:
        return False


def generate_opaque_token() -> str:
    """Generate a cryptographically secure opaque token."""
    return secrets.token_urlsafe(32)


def hash_opaque_token(token: str) -> str:
    """SHA-256 hash for storing opaque tokens at rest."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(
    subject: UUID | str,
    settings: Settings,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a JWT access token."""
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.effective_jwt_secret, algorithm=settings.algorithm)


def create_refresh_token_jwt(
    subject: UUID | str,
    settings: Settings,
    jti: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT wrapping the opaque refresh token id (jti)."""
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(days=settings.refresh_token_expire_days)
    )
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh",
        "jti": jti,
    }
    return jwt.encode(
        payload,
        settings.effective_jwt_refresh_secret,
        algorithm=settings.algorithm,
    )


def decode_token(token: str, settings: Settings) -> dict[str, Any]:
    """Decode and validate an access JWT; raises JWTError on failure."""
    return jwt.decode(token, settings.effective_jwt_secret, algorithms=[settings.algorithm])


def decode_refresh_token(token: str, settings: Settings) -> dict[str, Any]:
    """Decode and validate a refresh JWT; raises JWTError on failure."""
    return jwt.decode(
        token,
        settings.effective_jwt_refresh_secret,
        algorithms=[settings.algorithm],
    )


def verify_token_type(payload: dict[str, Any], expected_type: str) -> bool:
    """Ensure JWT payload has the expected token type claim."""
    return payload.get("type") == expected_type
