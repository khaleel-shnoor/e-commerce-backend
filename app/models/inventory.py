"""Inventory tracking model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.catalog import Product


class Inventory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Stock levels per product — supports reservation for checkout."""

    __tablename__ = "inventory"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    quantity_available: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    quantity_reserved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    warehouse_code: Mapped[str | None] = mapped_column(nullable=True, index=True)

    product: Mapped["Product"] = relationship(back_populates="inventory")
