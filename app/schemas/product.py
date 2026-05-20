"""Product catalog API schemas."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field

from app.models.enums import ProductStatus
from app.schemas.common import SchemaBase


class ProductImageResponse(SchemaBase):
    id: UUID
    url: str
    alt_text: str | None = None
    sort_order: int
    is_primary: bool


class ProductListItem(SchemaBase):
    id: UUID
    slug: str
    name: str
    price: Decimal
    compare_at_price: Decimal | None = None
    status: ProductStatus
    primary_image_url: str | None = None
    category_id: UUID | None = None
    category_name: str | None = None
    brand_name: str | None = None
    store_name: str | None = None
    quantity_available: int | None = None


class ProductDetailResponse(ProductListItem):
    description: str | None = None
    sku: str | None = None
    seller_id: UUID
    brand_id: UUID | None = None
    images: list[ProductImageResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ProductListResponse(SchemaBase):
    items: list[ProductListItem]
    total: int


class ProductCreateRequest(SchemaBase):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    sku: str | None = Field(default=None, max_length=64)
    price: Decimal = Field(gt=0)
    compare_at_price: Decimal | None = Field(default=None, gt=0)
    category_id: UUID | None = None
    brand_id: UUID | None = None
    status: ProductStatus = ProductStatus.DRAFT
    quantity_available: int = Field(default=0, ge=0)
    image_url: str | None = Field(default=None, max_length=512)
    image_alt: str | None = Field(default=None, max_length=255)


class ProductUpdateRequest(SchemaBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    sku: str | None = Field(default=None, max_length=64)
    price: Decimal | None = Field(default=None, gt=0)
    compare_at_price: Decimal | None = None
    category_id: UUID | None = None
    brand_id: UUID | None = None
    status: ProductStatus | None = None
    quantity_available: int | None = Field(default=None, ge=0)
    image_url: str | None = Field(default=None, max_length=512)
    image_alt: str | None = Field(default=None, max_length=255)


class CategoryResponse(SchemaBase):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    parent_id: UUID | None = None


class CategoryListResponse(SchemaBase):
    items: list[CategoryResponse]
