"""Authentication request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from app.models.enums import RoleName, SellerStatus
from app.schemas.common import SchemaBase


# class RegisterRequest(SchemaBase):
#     email: EmailStr
#     password: str = Field(min_length=8, max_length=128)
#     full_name: str | None = Field(default=None, max_length=255)
#     role: RoleName = RoleName.CUSTOMER

class RegisterRequest(SchemaBase):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)

    role: RoleName = RoleName.CUSTOMER

    store_name: str | None = Field(default=None, max_length=255)
    store_slug: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=2000)

class LoginRequest(SchemaBase):
    email: EmailStr
    password: str


class TokenResponse(SchemaBase):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(SchemaBase):
    refresh_token: str


class SellerProfileResponse(SchemaBase):
    id: UUID
    store_name: str
    store_slug: str
    status: SellerStatus
    description: str | None = None


class UserResponse(SchemaBase):
    id: UUID
    email: str
    full_name: str | None
    phone: str | None
    avatar_url: str | None = None
    is_active: bool
    is_verified: bool
    roles: list[str]
    seller: SellerProfileResponse | None = None
    created_at: datetime


class AuthResponse(SchemaBase):
    user: UserResponse
    tokens: TokenResponse


class VerifyEmailRequest(SchemaBase):
    token: str


class ResendVerificationRequest(SchemaBase):
    email: EmailStr


class ForgotPasswordRequest(SchemaBase):
    email: EmailStr


class ResetPasswordRequest(SchemaBase):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class OAuthCallbackResponse(SchemaBase):
    """Returned after Google OAuth — frontend receives tokens via redirect query."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
