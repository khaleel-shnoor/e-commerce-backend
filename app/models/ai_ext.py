"""AI-ready data models — embeddings, recommendations, search analytics."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.catalog import Product
    from app.models.user import User


class Embedding(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Vector embedding storage (pgvector column added in Phase 4)."""

    __tablename__ = "embeddings"
    __table_args__ = (
        UniqueConstraint("entity_type", "entity_id", "model_name", name="uq_embedding_entity"),
    )

    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    vector_data: Mapped[str | None] = mapped_column(Text, nullable=True)


class RecommendationScore(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Precomputed recommendation scores for users/products."""

    __tablename__ = "recommendation_scores"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", "algorithm", name="uq_rec_user_product_algo"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    algorithm: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    score: Mapped[Decimal] = mapped_column(Numeric(8, 6), nullable=False)

    user: Mapped["User"] = relationship()
    product: Mapped["Product"] = relationship()


class SearchAnalytic(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Search query analytics for ranking improvements."""

    __tablename__ = "search_analytics"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    query: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    results_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicked_product_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
    )
    session_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    user: Mapped["User | None"] = relationship()
    clicked_product: Mapped["Product | None"] = relationship()


class PersonalizationData(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User preference signals for AI personalization."""

    __tablename__ = "personalization_data"
    __table_args__ = (UniqueConstraint("user_id", "key", name="uq_personalization_user_key"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship()
