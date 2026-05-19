"""Extended commerce models — brands, variants, payments, returns."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PaymentStatus, ReturnStatus

if TYPE_CHECKING:
    from app.models.catalog import Category, Product
    from app.models.coupon import Coupon
    from app.models.order import Order
    from app.models.review import Review
    from app.models.user import User


class Brand(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Product brand master data."""

    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)

    products: Mapped[list["Product"]] = relationship(back_populates="brand")


class ProductVariant(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    """SKU variant (size, color, etc.)."""

    __tablename__ = "product_variants"
    __table_args__ = (UniqueConstraint("product_id", "sku", name="uq_variant_product_sku"),)

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    attributes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)

    product: Mapped["Product"] = relationship(back_populates="variants")


class ProductCategory(Base):
    """Many-to-many product ↔ category."""

    __tablename__ = "product_categories"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Payment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Order payment record."""

    __tablename__ = "payments"

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True,
    )
    provider: Mapped[str | None] = mapped_column(String(64), nullable=True)
    provider_reference: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    order: Mapped["Order"] = relationship(back_populates="payments")


class CouponUsage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tracks coupon redemption per user/order."""

    __tablename__ = "coupon_usages"
    __table_args__ = (UniqueConstraint("coupon_id", "user_id", "order_id", name="uq_coupon_usage"),)

    coupon_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("coupons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    coupon: Mapped["Coupon"] = relationship(back_populates="usages")
    user: Mapped["User"] = relationship()
    order: Mapped["Order"] = relationship()


class ReviewImage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Media attached to a product review."""

    __tablename__ = "review_images"

    review_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    review: Mapped["Review"] = relationship(back_populates="images")


class Return(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Product return request."""

    __tablename__ = "returns"

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ReturnStatus] = mapped_column(
        default=ReturnStatus.REQUESTED,
        nullable=False,
        index=True,
    )
    refund_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    order: Mapped["Order"] = relationship(back_populates="returns")
    user: Mapped["User"] = relationship()
