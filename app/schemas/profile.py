"""Profile update schemas."""

from pydantic import Field

from app.schemas.auth import UserResponse
from app.schemas.common import SchemaBase


class ProfileUpdateRequest(SchemaBase):
    full_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)


class ProfileResponse(UserResponse):
    """Current user profile — same shape as UserResponse."""
