"""Google OAuth integration via Authlib."""

from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.core.config import Settings
from app.core.exceptions import AuthenticationError, ValidationError
from app.core.security import hash_password
from app.models.auth import OAuthAccount
from app.models.enums import OAuthProvider, RoleName
from app.models.user import User
from app.repositories.auth import OAuthAccountRepository
from app.repositories.user import RoleRepository, UserRepository
from app.services.auth import AuthService

oauth = OAuth()


def configure_oauth(settings: Settings) -> None:
    """Register Google OAuth client if credentials are configured."""
    if not settings.google_client_id or not settings.google_client_secret:
        return
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


class OAuthService:
    """Google login/signup and account linking."""

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.users = UserRepository(session)
        self.roles = RoleRepository(session)
        self.oauth_accounts = OAuthAccountRepository(session)
        self.auth = AuthService(session, settings)

    def _google_configured(self) -> bool:
        return bool(self.settings.google_client_id and self.settings.google_client_secret)

    async def google_authorize_redirect(self, request: Request):
        if not self._google_configured():
            raise ValidationError("Google OAuth is not configured")
        redirect_uri = self.settings.google_redirect_uri
        return await oauth.google.authorize_redirect(request, redirect_uri)

    async def google_callback(self, request: Request):
        if not self._google_configured():
            raise ValidationError("Google OAuth is not configured")

        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get("userinfo")
        if not userinfo:
            raise AuthenticationError("Failed to retrieve Google user info")

        google_sub = userinfo["sub"]
        email = userinfo.get("email", "").lower()
        full_name = userinfo.get("name")

        if not email:
            raise AuthenticationError("Google account has no email")

        oauth_row = await self.oauth_accounts.get_by_provider(
            OAuthProvider.GOOGLE,
            google_sub,
        )
        if oauth_row:
            user = await self.users.get_with_roles(oauth_row.user_id)
            if user is None:
                raise AuthenticationError("Linked user not found")
            return await self.auth.issue_tokens_for_user(user)

        existing = await self.users.get_by_email(email)
        if existing:
            self.session.add(
                OAuthAccount(
                    user_id=existing.id,
                    provider=OAuthProvider.GOOGLE,
                    provider_user_id=google_sub,
                    provider_email=email,
                )
            )
            if not existing.is_verified:
                existing.is_verified = True
            await self.session.flush()
            user = await self.users.get_with_roles(existing.id)
            assert user is not None
            return await self.auth.issue_tokens_for_user(user)

        await self.auth._ensure_roles_seeded()
        role = await self.roles.get_by_name(RoleName.CUSTOMER)
        if role is None:
            raise ValidationError("Customer role not configured")

        user = User(
            email=email,
            password_hash=None,
            full_name=full_name,
            is_verified=True,
        )
        await self.users.add(user)
        await self.roles.assign_role(user, role)
        self.session.add(
            OAuthAccount(
                user_id=user.id,
                provider=OAuthProvider.GOOGLE,
                provider_user_id=google_sub,
                provider_email=email,
            )
        )
        await self.session.flush()
        user = await self.users.get_with_roles(user.id)
        assert user is not None
        return await self.auth.issue_tokens_for_user(user)
