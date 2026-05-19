"""User address model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AddressType

if TYPE_CHECKING:
    from app.models.user import User


class Address(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Shipping or billing address for a user."""

    __tablename__ = "addresses"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    address_type: Mapped[AddressType] = mapped_column(
        default=AddressType.SHIPPING,
        nullable=False,
    )
    label: Mapped[str | None] = mapped_column(String(64), nullable=True)
    line1: Mapped[str] = mapped_column(String(255), nullable=False)
    line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(128), nullable=False)
    state: Mapped[str | None] = mapped_column(String(128), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    user: Mapped["User"] = relationship(back_populates="addresses")
