"""
Future: Product embedding storage with pgvector (Phase 4).

Uncomment and add Alembic migration when pgvector extension is enabled:

    CREATE EXTENSION IF NOT EXISTS vector;

Example model (not active yet):

    class ProductEmbedding(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "product_embeddings"

        product_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("products.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        )
        embedding_model: Mapped[str] = mapped_column(String(64), nullable=False)
        # embedding: Mapped[list[float]] = mapped_column(Vector(1536))
"""
