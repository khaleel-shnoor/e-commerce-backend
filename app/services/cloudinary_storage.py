"""Cloudinary image upload service."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

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
MAX_PRODUCT_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB

AVATAR_TRANSFORMATION = [
    {"width": 400, "height": 400, "crop": "fill", "gravity": "face"},
]
PRODUCT_TRANSFORMATION = [
    {"width": 1200, "height": 1200, "crop": "limit", "quality": "auto"},
]


class CloudinaryStorage:
    """Upload user and product media to Cloudinary."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def is_configured(self) -> bool:
        return self.settings.cloudinary_ready

    def _upload_sync(
        self,
        file_bytes: bytes,
        public_id: str,
        *,
        transformation: list[dict[str, Any]] | None = None,
    ) -> str:
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=self.settings.cloudinary_cloud_name,
            api_key=self.settings.cloudinary_api_key,
            api_secret=self.settings.cloudinary_api_secret,
            secure=True,
        )
        folder = self.settings.cloudinary_folder
        upload_kwargs: dict[str, Any] = {
            "folder": folder,
            "public_id": public_id,
            "overwrite": True,
            "resource_type": "image",
        }
        if transformation:
            upload_kwargs["transformation"] = transformation

        result = cloudinary.uploader.upload(file_bytes, **upload_kwargs)
        return result["secure_url"]

    async def upload_avatar(self, file_bytes: bytes, user_id: str) -> str:
        if not self.is_configured:
            raise RuntimeError("Cloudinary is not configured")
        public_id = f"avatars/{user_id}"
        return await asyncio.to_thread(
            self._upload_sync,
            file_bytes,
            public_id,
            transformation=AVATAR_TRANSFORMATION,
        )

    async def upload_product_image(
        self,
        file_bytes: bytes,
        *,
        seller_id: str,
        product_id: str,
    ) -> str:
        if not self.is_configured:
            raise RuntimeError("Cloudinary is not configured")
        public_id = f"products/{seller_id}/{product_id}"
        return await asyncio.to_thread(
            self._upload_sync,
            file_bytes,
            public_id,
            transformation=PRODUCT_TRANSFORMATION,
        )
