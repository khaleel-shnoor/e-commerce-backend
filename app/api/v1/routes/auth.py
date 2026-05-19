"""Authentication API routes."""

from urllib.parse import urlencode

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from app.core.dependencies import AuthServiceDep, CurrentUser, DbSession, SettingsDep
from app.schemas.auth import (
    AuthResponse,
    ForgotPasswordRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    VerifyEmailRequest,
)
from app.schemas.common import MessageResponse
from app.services.oauth import OAuthService
from app.utils.user_response import to_user_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, auth: AuthServiceDep) -> AuthResponse:
    return await auth.register(body)


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, request: Request, auth: AuthServiceDep) -> AuthResponse:
    client = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    return await auth.login(body, user_agent=ua, ip=client)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(body: RefreshRequest, auth: AuthServiceDep) -> TokenResponse:
    return await auth.refresh(body.refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    auth: AuthServiceDep,
    body: RefreshRequest | None = None,
) -> MessageResponse:
    refresh = body.refresh_token if body else None
    await auth.logout(refresh)
    return MessageResponse(message="Logged out")


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser) -> UserResponse:
    return to_user_response(user)


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(body: VerifyEmailRequest, auth: AuthServiceDep) -> UserResponse:
    return await auth.verify_email(body)


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(
    body: ResendVerificationRequest,
    auth: AuthServiceDep,
) -> MessageResponse:
    await auth.resend_verification(body.email)
    return MessageResponse(message="If the email exists, a verification link was sent")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    body: ForgotPasswordRequest,
    auth: AuthServiceDep,
) -> MessageResponse:
    await auth.forgot_password(body)
    return MessageResponse(message="If the email exists, a reset link was sent")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(body: ResetPasswordRequest, auth: AuthServiceDep) -> MessageResponse:
    await auth.reset_password(body)
    return MessageResponse(message="Password updated successfully")


@router.get("/google/login")
async def google_login(request: Request, db: DbSession, settings: SettingsDep):
    """Redirect user to Google consent screen."""
    oauth_service = OAuthService(db, settings)
    return await oauth_service.google_authorize_redirect(request)


@router.get("/google/callback")
async def google_callback(request: Request, db: DbSession, settings: SettingsDep):
    """Handle Google OAuth callback and redirect to frontend with tokens."""
    oauth_service = OAuthService(db, settings)
    tokens = await oauth_service.google_callback(request)
    params = urlencode(
        {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "token_type": tokens.token_type,
        }
    )
    return RedirectResponse(url=f"{settings.frontend_url}/auth/callback?{params}")
