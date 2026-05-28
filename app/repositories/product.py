"""Product repository."""

import uuid
from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Wishlist, WishlistItem
from app.models.catalog import Product, ProductImage
from app.models.commerce_ext import Brand
from app.models.enums import ProductStatus, SellerStatus
from app.models.inventory import Inventory
from app.models.order import Order, OrderItem
from app.models.seller import Seller
from app.models.user import User
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Product)

    def _detail_options(self):
        return (
            selectinload(Product.images),
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.seller),
            selectinload(Product.inventory),
        )

    def _admin_detail_options(self):
        """Like _detail_options but also loads Seller.user for admin views."""
        return (
            selectinload(Product.images),
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.seller).selectinload(Seller.user),
            selectinload(Product.inventory),
        )

    async def get_for_admin(self, product_id: uuid.UUID) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(*self._admin_detail_options())
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(*self._detail_options())
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_seller_and_slug(self, seller_id: uuid.UUID, slug: str) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.seller_id == seller_id, Product.slug == slug)
            .options(*self._detail_options())
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_public_by_id(self, product_id: uuid.UUID) -> Product | None:
        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.id == product_id,
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
            )
            .options(*self._detail_options())
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_public_by_slug(self, slug: str) -> Product | None:
        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.slug == slug,
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
            )
            .options(*self._detail_options())
            .order_by(Product.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def slug_exists_for_seller(self, seller_id: uuid.UUID, slug: str) -> bool:
        stmt = (
            select(Product.id)
            .where(Product.seller_id == seller_id, Product.slug == slug)
            .limit(1)
        )
        result = await self.session.scalars(stmt)
        return result.first() is not None

    async def list_for_seller(
        self,
        seller_id: uuid.UUID,
        *,
        search: str | None = None,
        status: ProductStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.seller_id == seller_id)
            .options(*self._detail_options())
            .order_by(Product.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if status is not None:
            stmt = stmt.where(Product.status == status)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(Product.name.ilike(term), Product.sku.ilike(term), Product.slug.ilike(term))
            )
        result = await self.session.scalars(stmt)
        return list(result.unique().all())

    async def count_for_seller(
        self,
        seller_id: uuid.UUID,
        *,
        search: str | None = None,
        status: ProductStatus | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Product).where(Product.seller_id == seller_id)
        if status is not None:
            stmt = stmt.where(Product.status == status)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(Product.name.ilike(term), Product.sku.ilike(term), Product.slug.ilike(term))
            )
        result = await self.session.scalar(stmt)
        return int(result or 0)

    async def list_public(
        self,
        *,
        search: str | None = None,
        category_id: uuid.UUID | None = None,
        seller_id: uuid.UUID | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort: str = "newest",
        limit: int = 24,
        offset: int = 0,
    ) -> list[Product]:
        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
            )
            .options(*self._detail_options())
        )
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(Product.name.ilike(term), Product.description.ilike(term))
            )
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        if seller_id is not None:
            stmt = stmt.where(Product.seller_id == seller_id)
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)

        if sort == "price-asc":
            stmt = stmt.order_by(Product.price.asc())
        elif sort == "price-desc":
            stmt = stmt.order_by(Product.price.desc())
        elif sort == "name":
            stmt = stmt.order_by(Product.name.asc())
        else:
            stmt = stmt.order_by(Product.created_at.desc())

        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return list(result.unique().all())

    async def count_public(
        self,
        *,
        search: str | None = None,
        category_id: uuid.UUID | None = None,
        seller_id: uuid.UUID | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
            )
        )
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(Product.name.ilike(term), Product.description.ilike(term))
            )
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        if seller_id is not None:
            stmt = stmt.where(Product.seller_id == seller_id)
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
        result = await self.session.scalar(stmt)
        return int(result or 0)

    async def list_for_admin(
        self,
        *,
        status: ProductStatus | None = None,
        search: str | None = None,
        seller_id: uuid.UUID | None = None,
        exclude_id: uuid.UUID | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .options(*self._detail_options())
            .order_by(Product.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if status is not None:
            stmt = stmt.where(Product.status == status)
        if seller_id is not None:
            stmt = stmt.where(Product.seller_id == seller_id)
        if exclude_id is not None:
            stmt = stmt.where(Product.id != exclude_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(or_(Product.name.ilike(term), Product.sku.ilike(term)))
        result = await self.session.scalars(stmt)
        return list(result.unique().all())

    async def count_for_admin(
        self,
        *,
        status: ProductStatus | None = None,
        search: str | None = None,
        seller_id: uuid.UUID | None = None,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(Product)
            .join(Seller, Product.seller_id == Seller.id)
        )
        if status is not None:
            stmt = stmt.where(Product.status == status)
        if seller_id is not None:
            stmt = stmt.where(Product.seller_id == seller_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(or_(Product.name.ilike(term), Product.sku.ilike(term)))
        result = await self.session.scalar(stmt)
        return int(result or 0)

    async def list_related(
        self,
        category_id: uuid.UUID | None,
        exclude_id: uuid.UUID,
        limit: int = 4,
    ) -> list[Product]:
        """Same-category products, excluding the current one. Falls back to newest if no category."""
        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
                Product.id != exclude_id,
            )
            .options(*self._detail_options())
            .order_by(Product.created_at.desc())
            .limit(limit)
        )
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        result = await self.session.scalars(stmt)
        return list(result.unique().all())

    async def list_recommended(
        self,
        user_id: uuid.UUID,
        limit: int = 8,
    ) -> list[Product]:
        """Products recommended for a user based on order + wishlist category history.

        Falls back to newest active products when the user has no history yet.
        """
        # Collect category_ids from order history
        order_cat_stmt = (
            select(Product.category_id)
            .join(OrderItem, OrderItem.product_id == Product.id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.user_id == user_id, Product.category_id.is_not(None))
            .distinct()
        )
        # Collect category_ids from wishlist
        wishlist_cat_stmt = (
            select(Product.category_id)
            .join(WishlistItem, WishlistItem.product_id == Product.id)
            .join(Wishlist, Wishlist.id == WishlistItem.wishlist_id)
            .where(Wishlist.user_id == user_id, Product.category_id.is_not(None))
            .distinct()
        )
        # Already-ordered product ids to exclude
        ordered_ids_stmt = (
            select(OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.user_id == user_id)
        )

        category_ids = list((await self.session.scalars(order_cat_stmt)).all())
        category_ids += [
            cid
            for cid in (await self.session.scalars(wishlist_cat_stmt)).all()
            if cid not in category_ids
        ]
        ordered_product_ids = list((await self.session.scalars(ordered_ids_stmt)).all())

        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
            )
            .options(*self._detail_options())
            .limit(limit)
        )

        if category_ids:
            stmt = stmt.where(Product.category_id.in_(category_ids))
            stmt = stmt.order_by(func.random())
        else:
            stmt = stmt.order_by(Product.created_at.desc())

        if ordered_product_ids:
            stmt = stmt.where(Product.id.notin_(ordered_product_ids))

        result = await self.session.scalars(stmt)
        return list(result.unique().all())

    async def add_image(self, image: ProductImage) -> ProductImage:
        self.session.add(image)
        await self.session.flush()
        return image

    async def add_inventory(self, inventory: Inventory) -> Inventory:
        self.session.add(inventory)
        await self.session.flush()
        return inventory
