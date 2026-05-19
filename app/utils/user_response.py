"""Map ORM User to API response DTO."""

from app.models.user import User
from app.schemas.auth import UserResponse


def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        is_active=user.is_active,
        is_verified=user.is_verified,
        roles=[r.name.value for r in user.roles],
        created_at=user.created_at,
    )
