"""Cloudinary image upload service."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.config import Settings

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}
MAX_AVATAR_BYTES = 5 * 1024 * 1024  # 5 MB


class CloudinaryStorage:
    """Upload user media to Cloudinary."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def is_configured(self) -> bool:
        return self.settings.cloudinary_ready

    def _upload_sync(self, file_bytes: bytes, public_id: str) -> str:
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=self.settings.cloudinary_cloud_name,
            api_key=self.settings.cloudinary_api_key,
            api_secret=self.settings.cloudinary_api_secret,
            secure=True,
        )
        folder = self.settings.cloudinary_folder
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=folder,
            public_id=public_id,
            overwrite=True,
            resource_type="image",
            transformation=[{"width": 400, "height": 400, "crop": "fill", "gravity": "face"}],
        )
        return result["secure_url"]

    async def upload_avatar(self, file_bytes: bytes, user_id: str) -> str:
        if not self.is_configured:
            raise RuntimeError("Cloudinary is not configured")
        public_id = f"avatars/{user_id}"
        return await asyncio.to_thread(self._upload_sync, file_bytes, public_id)
