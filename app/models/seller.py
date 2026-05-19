"""Seller and admin profile models."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import SellerStatus

if TYPE_CHECKING:
    from app.models.catalog import Product
    from app.models.seller_ext import SellerDocument, SellerPayout, SellerSettings, SellerWallet
    from app.models.user import User


class Seller(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Seller business profile linked to a user account."""

    __tablename__ = "sellers"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    store_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    store_slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[SellerStatus] = mapped_column(
        default=SellerStatus.PENDING,
        nullable=False,
        index=True,
    )
    commission_rate: Mapped[float | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="seller_profile")
    products: Mapped[list["Product"]] = relationship(back_populates="seller")
    documents: Mapped[list["SellerDocument"]] = relationship(
        back_populates="seller",
        cascade="all, delete-orphan",
    )
    payouts: Mapped[list["SellerPayout"]] = relationship(
        back_populates="seller",
        cascade="all, delete-orphan",
    )
    wallet: Mapped["SellerWallet | None"] = relationship(
        back_populates="seller",
        uselist=False,
        cascade="all, delete-orphan",
    )
    settings: Mapped["SellerSettings | None"] = relationship(
        back_populates="seller",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Admin(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Admin profile linked to a user account."""

    __tablename__ = "admins"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    department: Mapped[str | None] = mapped_column(String(128), nullable=True)
    title: Mapped[str | None] = mapped_column(String(128), nullable=True)

    user: Mapped["User"] = relationship(back_populates="admin_profile")
