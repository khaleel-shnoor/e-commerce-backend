"""Admin panel API schemas."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.models.enums import ProductStatus, SellerStatus
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


class AdminProductItem(SchemaBase):
    id: UUID
    name: str
    slug: str
    price: Decimal
    status: ProductStatus
    primary_image_url: str | None = None
    category_name: str | None = None
    seller_id: UUID
    store_name: str
    store_slug: str
    quantity_available: int | None = None
    created_at: datetime


class AdminProductsListResponse(SchemaBase):
    items: list[AdminProductItem]
    total: int


class UpdateProductStatusRequest(SchemaBase):
    status: ProductStatus


class AdminProductImageItem(SchemaBase):
    id: UUID
    url: str
    alt_text: str | None = None
    sort_order: int
    is_primary: bool


class AdminSellerSummary(SchemaBase):
    id: UUID
    store_name: str
    store_slug: str
    status: SellerStatus
    description: str | None = None
    email: str
    full_name: str | None = None
    joined_at: datetime


class AdminProductDetailResponse(SchemaBase):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    sku: str | None = None
    price: Decimal
    compare_at_price: Decimal | None = None
    status: ProductStatus
    category_id: UUID | None = None
    category_name: str | None = None
    brand_name: str | None = None
    quantity_available: int | None = None
    images: list[AdminProductImageItem]
    created_at: datetime
    updated_at: datetime
    seller: AdminSellerSummary
    seller_products: list[AdminProductItem]
