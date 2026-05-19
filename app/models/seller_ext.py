"""Extended seller models — documents, payouts, wallet, settings."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PayoutStatus, SellerStatus

if TYPE_CHECKING:
    from app.models.seller import Seller


class SellerDocument(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """KYC / verification documents for sellers."""

    __tablename__ = "seller_documents"

    seller_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    file_url: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[SellerStatus] = mapped_column(
        default=SellerStatus.PENDING,
        nullable=False,
        index=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    seller: Mapped["Seller"] = relationship(back_populates="documents")


class SellerPayout(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Seller payout disbursement record."""

    __tablename__ = "seller_payouts"

    seller_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[PayoutStatus] = mapped_column(
        default=PayoutStatus.PENDING,
        nullable=False,
        index=True,
    )
    reference: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    seller: Mapped["Seller"] = relationship(back_populates="payouts")


class SellerWallet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Seller balance wallet — one per seller."""

    __tablename__ = "seller_wallets"

    seller_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    pending_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)

    seller: Mapped["Seller"] = relationship(back_populates="wallet", uselist=False)


class SellerSettings(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Per-seller store configuration."""

    __tablename__ = "seller_settings"

    seller_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    auto_fulfill: Mapped[bool] = mapped_column(default=False, nullable=False)
    notification_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    return_policy: Mapped[str | None] = mapped_column(Text, nullable=True)
    shipping_policy: Mapped[str | None] = mapped_column(Text, nullable=True)
    theme_config: Mapped[str | None] = mapped_column(Text, nullable=True)

    seller: Mapped["Seller"] = relationship(back_populates="settings", uselist=False)
