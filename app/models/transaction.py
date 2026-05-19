"""Financial transaction model — payment gateway integration in Phase 2."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import TransactionStatus, TransactionType

if TYPE_CHECKING:
    from app.models.order import Order


class Transaction(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Payment, refund, or seller payout record."""

    __tablename__ = "transactions"

    order_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("orders.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    reference: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    transaction_type: Mapped[TransactionType] = mapped_column(nullable=False, index=True)
    status: Mapped[TransactionStatus] = mapped_column(
        default=TransactionStatus.PENDING,
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    gateway: Mapped[str | None] = mapped_column(String(64), nullable=True)
    gateway_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)

    order: Mapped["Order | None"] = relationship(back_populates="transactions")
