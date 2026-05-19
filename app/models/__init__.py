"""
ORM models package — import all models so Alembic autogenerate detects metadata.
"""

from app.models.address import Address
from app.models.admin_ext import AdminLog, Banner, CmsPage, Report, SupportTicket
from app.models.ai_ext import Embedding, PersonalizationData, RecommendationScore, SearchAnalytic
from app.models.auth import (
    EmailVerificationToken,
    OAuthAccount,
    PasswordResetToken,
    RefreshToken,
    UserSession,
)
from app.models.base import Base
from app.models.cart import Cart, CartItem, Wishlist, WishlistItem
from app.models.catalog import Category, Product, ProductImage
from app.models.commerce_ext import (
    Brand,
    CouponUsage,
    Payment,
    ProductCategory,
    ProductVariant,
    Return,
    ReviewImage,
)
from app.models.coupon import Coupon
from app.models.inventory import Inventory
from app.models.notification import Notification
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.seller import Admin, Seller
from app.models.seller_ext import SellerDocument, SellerPayout, SellerSettings, SellerWallet
from app.models.system_ext import ActivityLog, AuditLog, NotificationPreference
from app.models.transaction import Transaction
from app.models.user import Role, User, UserRole

__all__ = [
    "Base",
    "User",
    "Role",
    "UserRole",
    "RefreshToken",
    "OAuthAccount",
    "PasswordResetToken",
    "EmailVerificationToken",
    "UserSession",
    "Seller",
    "Admin",
    "SellerDocument",
    "SellerPayout",
    "SellerWallet",
    "SellerSettings",
    "Category",
    "Product",
    "ProductImage",
    "Brand",
    "ProductVariant",
    "ProductCategory",
    "Cart",
    "CartItem",
    "Wishlist",
    "WishlistItem",
    "Order",
    "OrderItem",
    "Payment",
    "Return",
    "Review",
    "ReviewImage",
    "Inventory",
    "Address",
    "Coupon",
    "CouponUsage",
    "Notification",
    "NotificationPreference",
    "Transaction",
    "AdminLog",
    "Report",
    "SupportTicket",
    "Banner",
    "CmsPage",
    "AuditLog",
    "ActivityLog",
    "Embedding",
    "RecommendationScore",
    "SearchAnalytic",
    "PersonalizationData",
]
