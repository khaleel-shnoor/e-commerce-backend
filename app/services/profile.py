"""User profile business logic."""

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.exceptions import NotFoundError, ValidationError
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.profile import ProfileUpdateRequest
from app.services.cloudinary_storage import ALLOWED_CONTENT_TYPES, MAX_AVATAR_BYTES, CloudinaryStorage
from app.utils.user_response import to_user_response


class ProfileService:
    """Fetch and update the authenticated user's profile."""

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.users = UserRepository(session)
        self.storage = CloudinaryStorage(settings)

    async def get_profile(self, user: User):
        loaded = await self.users.get_with_roles(user.id)
        if loaded is None:
            raise NotFoundError("User not found")
        return to_user_response(loaded)

    async def update_profile(self, user: User, data: ProfileUpdateRequest):
        loaded = await self.users.get_with_roles(user.id)
        if loaded is None:
            raise NotFoundError("User not found")

        if data.full_name is not None:
            loaded.full_name = data.full_name.strip() or None
        if data.phone is not None:
            loaded.phone = data.phone.strip() or None

        await self.session.flush()
        await self.session.refresh(loaded)
        return to_user_response(loaded)

    async def upload_avatar(self, user: User, file: UploadFile):
        if not self.storage.is_configured:
            raise ValidationError(
                "Image upload is not configured. Set CLOUDINARY_* variables in .env"
            )

        content_type = file.content_type or ""
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError("Allowed formats: JPEG, PNG, WebP, GIF")

        file_bytes = await file.read()
        if not file_bytes:
            raise ValidationError("Empty file")
        if len(file_bytes) > MAX_AVATAR_BYTES:
            raise ValidationError("Image must be 5 MB or smaller")

        url = await self.storage.upload_avatar(file_bytes, str(user.id))

        loaded = await self.users.get_with_roles(user.id)
        if loaded is None:
            raise NotFoundError("User not found")
        loaded.avatar_url = url
        await self.session.flush()
        await self.session.refresh(loaded)
        return to_user_response(loaded)
