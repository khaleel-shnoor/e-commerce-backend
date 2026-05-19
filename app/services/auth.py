"""Authentication business logic."""

import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.exceptions import AuthenticationError, ConflictError, NotFoundError, ValidationError
from app.core.security import (
    create_access_token,
    create_refresh_token_jwt,
    decode_refresh_token,
    generate_opaque_token,
    hash_opaque_token,
    hash_password,
    verify_password,
    verify_token_type,
)
from app.models.auth import EmailVerificationToken, PasswordResetToken, RefreshToken
from app.models.enums import RoleName, TokenPurpose
from app.models.user import User
from app.repositories.auth import (
    EmailVerificationTokenRepository,
    PasswordResetTokenRepository,
    RefreshTokenRepository,
)
from app.repositories.user import RoleRepository, UserRepository
from app.schemas.auth import (
    AuthResponse,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    VerifyEmailRequest,
)
from app.services.email import EmailService
from app.utils.user_response import to_user_response


class AuthService:
    """Handles registration, login, tokens, and password flows."""

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.users = UserRepository(session)
        self.roles = RoleRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)
        self.reset_tokens = PasswordResetTokenRepository(session)
        self.verify_tokens = EmailVerificationTokenRepository(session)
        self.email = EmailService(settings)

    async def _ensure_roles_seeded(self) -> None:
        for role_name in RoleName:
            existing = await self.roles.get_by_name(role_name)
            if existing is None:
                from app.models.user import Role

                await self.roles.add(Role(name=role_name, description=f"{role_name.value} role"))

    async def _issue_tokens(
        self,
        user: User,
        *,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> TokenResponse:
        opaque = generate_opaque_token()
        token_hash = hash_opaque_token(opaque)
        expires_at = datetime.now(UTC) + timedelta(days=self.settings.refresh_token_expire_days)

        refresh_row = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        await self.refresh_tokens.add(refresh_row)

        access = create_access_token(
            user.id,
            self.settings,
            extra_claims={"roles": [r.name.value for r in user.roles]},
        )
        refresh_jwt = create_refresh_token_jwt(user.id, self.settings, jti=str(refresh_row.id))

        return TokenResponse(
            access_token=access,
            refresh_token=refresh_jwt,
            expires_in=self.settings.access_token_expire_minutes * 60,
        )

    async def register(self, data: RegisterRequest) -> AuthResponse:
        await self._ensure_roles_seeded()
        email = data.email.lower()

        if await self.users.get_by_email(email):
            raise ConflictError("Email already registered")

        role = await self.roles.get_by_name(data.role)
        if role is None:
            raise ValidationError(f"Role {data.role.value} not configured")

        user = User(
            email=email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            is_verified=False,
        )
        await self.users.add(user)
        await self.roles.assign_role(user, role)
        user = await self.users.get_with_roles(user.id)
        assert user is not None

        await self._send_verification_email(user)
        tokens = await self._issue_tokens(user)
        return AuthResponse(user=to_user_response(user), tokens=tokens)

    async def login(self, data: LoginRequest, *, user_agent: str | None = None, ip: str | None = None) -> AuthResponse:
        user = await self.users.get_by_email(data.email.lower())
        if user is None or not verify_password(data.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")
        if not user.is_active:
            raise AuthenticationError("Account is disabled")

        tokens = await self._issue_tokens(user, user_agent=user_agent, ip_address=ip)
        return AuthResponse(user=to_user_response(user), tokens=tokens)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_refresh_token(refresh_token, self.settings)
        except JWTError as exc:
            raise AuthenticationError("Invalid refresh token") from exc

        if not verify_token_type(payload, "refresh"):
            raise AuthenticationError("Invalid token type")

        jti = payload.get("jti")
        if not jti:
            raise AuthenticationError("Invalid refresh token")

        try:
            refresh_id = uuid.UUID(jti)
        except ValueError as exc:
            raise AuthenticationError("Invalid refresh token") from exc

        stored = await self.refresh_tokens.get_by_id(refresh_id)
        if stored is None or stored.revoked_at is not None:
            raise AuthenticationError("Refresh token revoked or expired")
        if stored.expires_at < datetime.now(UTC):
            raise AuthenticationError("Refresh token expired")

        await self.refresh_tokens.revoke(stored)
        user = await self.users.get_with_roles(stored.user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("User not found or inactive")

        return await self._issue_tokens(user)

    async def logout(self, refresh_token: str | None) -> None:
        if not refresh_token:
            return
        try:
            payload = decode_refresh_token(refresh_token, self.settings)
            jti = payload.get("jti")
            if jti:
                stored = await self.refresh_tokens.get_by_id(uuid.UUID(jti))
                if stored:
                    await self.refresh_tokens.revoke(stored)
        except (JWTError, ValueError):
            pass

    async def get_current_user(self, user_id: uuid.UUID) -> User:
        user = await self.users.get_with_roles(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        return user

    async def _send_verification_email(self, user: User) -> str:
        raw = generate_opaque_token()
        token = EmailVerificationToken(
            user_id=user.id,
            token_hash=hash_opaque_token(raw),
            purpose=TokenPurpose.EMAIL_VERIFICATION,
            expires_at=datetime.now(UTC)
            + timedelta(hours=self.settings.email_verification_expire_hours),
        )
        await self.verify_tokens.add(token)
        await self.email.send_verification(user.email, raw)
        return raw

    async def verify_email(self, data: VerifyEmailRequest) -> UserResponse:
        token_hash = hash_opaque_token(data.token)
        row = await self.verify_tokens.get_valid_by_hash(token_hash)
        if row is None:
            raise ValidationError("Invalid or expired verification token")

        user = await self.users.get_with_roles(row.user_id)
        if user is None:
            raise NotFoundError("User not found")

        user.is_verified = True
        await self.verify_tokens.mark_used(row)
        await self.session.flush()
        return to_user_response(user)

    async def resend_verification(self, email: str) -> None:
        user = await self.users.get_by_email(email.lower())
        if user is None or user.is_verified:
            return
        await self._send_verification_email(user)

    async def forgot_password(self, data: ForgotPasswordRequest) -> None:
        user = await self.users.get_by_email(data.email.lower())
        if user is None:
            return

        await self.reset_tokens.invalidate_user_tokens(user.id)
        raw = generate_opaque_token()
        row = PasswordResetToken(
            user_id=user.id,
            token_hash=hash_opaque_token(raw),
            expires_at=datetime.now(UTC)
            + timedelta(minutes=self.settings.password_reset_expire_minutes),
        )
        await self.reset_tokens.add(row)
        await self.email.send_password_reset(user.email, raw)

    async def reset_password(self, data: ResetPasswordRequest) -> None:
        token_hash = hash_opaque_token(data.token)
        row = await self.reset_tokens.get_valid_by_hash(token_hash)
        if row is None:
            raise ValidationError("Invalid or expired reset token")

        user = await self.users.get_by_id(row.user_id)
        if user is None:
            raise NotFoundError("User not found")

        user.password_hash = hash_password(data.new_password)
        await self.reset_tokens.mark_used(row)
        await self.refresh_tokens.revoke_all_for_user(user.id)

    async def issue_tokens_for_user(
        self,
        user: User,
        *,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> TokenResponse:
        """Used by OAuth after user resolution."""
        user = await self.users.get_with_roles(user.id)
        assert user is not None
        return await self._issue_tokens(user, user_agent=user_agent, ip_address=ip_address)
