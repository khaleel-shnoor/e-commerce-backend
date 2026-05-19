"""Auth tables and extended commerce schema.

Revision ID: 20260518_002
Revises: 20260518_001
Create Date: 2026-05-18
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20260518_002"
down_revision: Union[str, None] = "20260518_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create new tables from updated SQLAlchemy metadata."""
    import app.models  # noqa: F401
    from app.models.base import Base

    bind = op.get_bind()
    # create_all only creates missing tables; existing foundation tables unchanged
    Base.metadata.create_all(bind)


def downgrade() -> None:
    """Drop extension tables (auth + extensions). Manual care on production."""
    import app.models  # noqa: F401
    from sqlalchemy import MetaData

    from app.models.auth import (
        EmailVerificationToken,
        OAuthAccount,
        PasswordResetToken,
        RefreshToken,
        UserSession,
    )
    from app.models.admin_ext import AdminLog, Banner, CmsPage, Report, SupportTicket
    from app.models.ai_ext import Embedding, PersonalizationData, RecommendationScore, SearchAnalytic
    from app.models.commerce_ext import (
        Brand,
        CouponUsage,
        Payment,
        ProductCategory,
        ProductVariant,
        Return,
        ReviewImage,
    )
    from app.models.seller_ext import SellerDocument, SellerPayout, SellerSettings, SellerWallet
    from app.models.system_ext import ActivityLog, AuditLog, NotificationPreference
    from app.models.cart import WishlistItem

    extension_tables = [
        WishlistItem.__table__,
        RefreshToken.__table__,
        OAuthAccount.__table__,
        PasswordResetToken.__table__,
        EmailVerificationToken.__table__,
        UserSession.__table__,
        Brand.__table__,
        ProductVariant.__table__,
        ProductCategory.__table__,
        Payment.__table__,
        CouponUsage.__table__,
        ReviewImage.__table__,
        Return.__table__,
        SellerDocument.__table__,
        SellerPayout.__table__,
        SellerWallet.__table__,
        SellerSettings.__table__,
        AdminLog.__table__,
        Report.__table__,
        SupportTicket.__table__,
        Banner.__table__,
        CmsPage.__table__,
        NotificationPreference.__table__,
        AuditLog.__table__,
        ActivityLog.__table__,
        Embedding.__table__,
        RecommendationScore.__table__,
        SearchAnalytic.__table__,
        PersonalizationData.__table__,
    ]

    bind = op.get_bind()
    meta = MetaData()
    for table in extension_tables:
        table.tometadata(meta)
    meta.drop_all(bind)
