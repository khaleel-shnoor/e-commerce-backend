"""Discount coupon model."""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.commerce_ext import CouponUsage
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import CouponDiscountType


class Coupon(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Promotional coupon — redemption logic in Phase 2."""

    __tablename__ = "coupons"

    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    discount_type: Mapped[CouponDiscountType] = mapped_column(nullable=False)
    discount_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    min_order_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    max_uses: Mapped[int | None] = mapped_column(nullable=True)
    uses_count: Mapped[int] = mapped_column(default=0, nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)

    usages: Mapped[list["CouponUsage"]] = relationship(
        back_populates="coupon",
        cascade="all, delete-orphan",
    )
