"""Order, cart, wishlist, and address API schemas."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field

from app.models.enums import OrderStatus
from app.schemas.common import SchemaBase


# ── Address ───────────────────────────────────────────────────────────────────

class AddressCreate(SchemaBase):
    label: str | None = Field(default=None, max_length=64)
    line1: str = Field(min_length=1, max_length=255)
    line2: str | None = Field(default=None, max_length=255)
    city: str = Field(min_length=1, max_length=128)
    state: str | None = Field(default=None, max_length=128)
    postal_code: str = Field(min_length=1, max_length=32)
    country: str = Field(min_length=2, max_length=2)
    is_default: bool = False


class AddressUpdate(SchemaBase):
    label: str | None = None
    line1: str | None = Field(default=None, min_length=1, max_length=255)
    line2: str | None = None
    city: str | None = Field(default=None, min_length=1, max_length=128)
    state: str | None = None
    postal_code: str | None = Field(default=None, min_length=1, max_length=32)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    is_default: bool | None = None


class AddressResponse(SchemaBase):
    id: UUID
    label: str | None
    line1: str
    line2: str | None
    city: str
    state: str | None
    postal_code: str
    country: str
    is_default: bool
    created_at: datetime


class AddressListResponse(SchemaBase):
    items: list[AddressResponse]


# ── Wishlist ──────────────────────────────────────────────────────────────────

class WishlistItemResponse(SchemaBase):
    id: UUID
    product_id: UUID
    product_name: str
    product_price: Decimal
    product_image_url: str | None
    product_slug: str
    added_at: datetime


class WishlistResponse(SchemaBase):
    items: list[WishlistItemResponse]
    total: int


class WishlistToggleResponse(SchemaBase):
    in_wishlist: bool
    product_id: UUID


# ── Cart ──────────────────────────────────────────────────────────────────────

class CartItemResponse(SchemaBase):
    id: UUID
    product_id: UUID
    product_name: str
    product_price: Decimal
    product_image_url: str | None
    product_slug: str
    quantity: int
    line_total: Decimal


class CartResponse(SchemaBase):
    items: list[CartItemResponse]
    subtotal: Decimal
    item_count: int


class CartAddRequest(SchemaBase):
    product_id: UUID
    quantity: int = Field(default=1, ge=1, le=100)


class CartUpdateRequest(SchemaBase):
    quantity: int = Field(ge=1, le=100)


# ── Orders ────────────────────────────────────────────────────────────────────

class ShippingAddressSnapshot(SchemaBase):
    line1: str
    line2: str | None
    city: str
    state: str | None
    postal_code: str
    country: str


class OrderItemResponse(SchemaBase):
    id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class OrderListItem(SchemaBase):
    id: UUID
    order_number: str
    status: OrderStatus
    total_amount: Decimal
    item_count: int
    created_at: datetime


class OrderDetailResponse(SchemaBase):
    id: UUID
    order_number: str
    status: OrderStatus
    subtotal: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    notes: str | None
    items: list[OrderItemResponse]
    shipping_address: AddressResponse | None
    payment_method: str
    created_at: datetime
    updated_at: datetime


class OrderListResponse(SchemaBase):
    items: list[OrderListItem]
    total: int


class CheckoutRequest(SchemaBase):
    """Payload to place an order from the active cart."""
    shipping_address_id: UUID | None = None
    new_address: AddressCreate | None = None
    notes: str | None = Field(default=None, max_length=500)


# ── Seller order view ─────────────────────────────────────────────────────────

class SellerOrderItemResponse(SchemaBase):
    order_id: UUID
    order_number: str
    order_status: OrderStatus
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal
    buyer_name: str | None
    buyer_email: str
    ordered_at: datetime


class SellerOrderListResponse(SchemaBase):
    items: list[SellerOrderItemResponse]
    total: int


# ── Analytics ─────────────────────────────────────────────────────────────────

class RevenueDataPoint(SchemaBase):
    month: str
    revenue: Decimal
    orders: int


class SellerAnalyticsResponse(SchemaBase):
    revenue: Decimal
    orders: int
    products: int
    revenue_by_month: list[RevenueDataPoint]
    top_products: list[dict]
    recent_orders: list[SellerOrderItemResponse]


class AdminAnalyticsResponse(SchemaBase):
    total_revenue: Decimal
    total_orders: int
    total_users: int
    total_sellers: int
    revenue_by_month: list[RevenueDataPoint]
    recent_orders: list[dict]
