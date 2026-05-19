"""FastAPI dependency injection for DB sessions and shared resources."""

from collections.abc import AsyncGenerator, Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token, verify_token_type
from app.models.enums import RoleName
from app.models.user import User
from app.services.auth import AuthService
from app.services.email import EmailService
from app.services.profile import ProfileService

bearer_scheme = HTTPBearer(auto_error=False)


def get_db_manager(request: Request):
    """Return the application-scoped DatabaseSessionManager."""
    return request.app.state.db_manager


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession]:
    """Yield an async database session for the current request."""
    db_manager = request.app.state.db_manager
    async for session in db_manager.session():
        yield session


def get_email_service(settings: "SettingsDep") -> EmailService:
    return EmailService(settings)


def get_auth_service(
    db: "DbSession",
    settings: "SettingsDep",
) -> AuthService:
    return AuthService(db, settings)


def get_profile_service(db: "DbSession", settings: "SettingsDep") -> ProfileService:
    return ProfileService(db, settings)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: "DbSession",
    settings: "SettingsDep",
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("Not authenticated")

    try:
        payload = decode_token(credentials.credentials, settings)
    except JWTError as exc:
        raise AuthenticationError("Invalid token") from exc

    if not verify_token_type(payload, "access"):
        raise AuthenticationError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid token subject")

    auth = AuthService(db, settings)
    return await auth.get_current_user(UUID(user_id))


def require_roles(*allowed: RoleName) -> Callable:
    """Dependency factory for role-based access control."""

    async def _checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        user_roles = {r.name for r in user.roles}
        if not user_roles.intersection(set(allowed)):
            raise AuthorizationError(
                f"Requires one of: {', '.join(r.value for r in allowed)}"
            )
        return user

    return _checker


DbSession = Annotated[AsyncSession, Depends(get_db_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
EmailServiceDep = Annotated[EmailService, Depends(get_email_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ProfileServiceDep = Annotated[ProfileService, Depends(get_profile_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
