"""Admin panel API schemas."""

from datetime import datetime
from uuid import UUID

from app.models.enums import SellerStatus
from app.schemas.common import SchemaBase


class AdminUserItem(SchemaBase):
    id: UUID
    email: str
    full_name: str | None
    phone: str | None
    roles: list[str]
    is_active: bool
    is_verified: bool
    has_password: bool
    created_at: datetime


class AdminSellerItem(SchemaBase):
    id: UUID
    user_id: UUID
    email: str
    full_name: str | None
    store_name: str
    store_slug: str
    status: SellerStatus
    user_is_active: bool
    user_is_verified: bool
    created_at: datetime


class AdminUsersListResponse(SchemaBase):
    items: list[AdminUserItem]
    total: int


class AdminSellersListResponse(SchemaBase):
    items: list[AdminSellerItem]
    total: int


class UpdateSellerStatusRequest(SchemaBase):
    status: SellerStatus
