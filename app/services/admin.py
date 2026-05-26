"""Admin panel business logic."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationError
from app.models.catalog import Product
from app.models.enums import ProductStatus, RoleName, SellerStatus
from app.models.seller import Seller
from app.models.user import User
from app.repositories.product import ProductRepository
from app.repositories.seller import SellerRepository
from app.repositories.user import UserRepository
from app.schemas.admin import (
    AdminProductDetailResponse,
    AdminProductImageItem,
    AdminProductItem,
    AdminSellerItem,
    AdminSellerSummary,
    AdminUserItem,
)


class AdminService:
    """List and manage platform users, sellers, and products."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.sellers = SellerRepository(session)
        self.products = ProductRepository(session)

    async def list_users(
        self,
        *,
        search: str | None = None,
        role: RoleName | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AdminUserItem], int]:
        rows = await self.users.list_with_roles(
            search=search,
            role=role,
            limit=limit,
            offset=offset,
        )
        return [_to_admin_user(u) for u in rows], len(rows)

    async def list_sellers(
        self,
        *,
        search: str | None = None,
        status: SellerStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AdminSellerItem], int]:
        rows = await self.sellers.list_with_users(
            search=search,
            status=status,
            limit=limit,
            offset=offset,
        )
        return [_to_admin_seller(s) for s in rows], len(rows)

    async def update_seller_status(
        self,
        seller_id: uuid.UUID,
        *,
        status: SellerStatus,
    ) -> AdminSellerItem:
        seller = await self.sellers.get_by_id_with_user(seller_id)
        if seller is None:
            raise NotFoundError("Seller not found")
        seller.status = status
        await self.session.flush()
        return _to_admin_seller(seller)

    async def list_products(
        self,
        *,
        status: ProductStatus | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[AdminProductItem], int]:
        rows = await self.products.list_for_admin(
            status=status,
            search=search,
            limit=limit,
            offset=offset,
        )
        total = await self.products.count_for_admin(status=status, search=search)
        return [_to_admin_product(p) for p in rows], total

    async def get_product_detail(self, product_id: uuid.UUID) -> AdminProductDetailResponse:
        product = await self.products.get_for_admin(product_id)
        if product is None:
            raise NotFoundError("Product not found")

        seller_products = await self.products.list_for_admin(
            seller_id=product.seller_id,
            exclude_id=product.id,
            limit=20,
        )

        return _to_admin_product_detail(product, seller_products)

    async def update_product_status(
        self,
        product_id: uuid.UUID,
        *,
        status: ProductStatus,
    ) -> AdminProductItem:
        product = await self.products.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found")
        product.status = status
        await self.session.flush()
        product = await self.products.get_by_id(product_id)
        assert product is not None
        return _to_admin_product(product)


def _to_admin_user(user: User) -> AdminUserItem:
    return AdminUserItem(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        roles=[r.name.value for r in user.roles],
        is_active=user.is_active,
        is_verified=user.is_verified,
        has_password=user.password_hash is not None,
        created_at=user.created_at,
    )


def _to_admin_seller(seller: Seller) -> AdminSellerItem:
    user = seller.user
    return AdminSellerItem(
        id=seller.id,
        user_id=seller.user_id,
        email=user.email,
        full_name=user.full_name,
        store_name=seller.store_name,
        store_slug=seller.store_slug,
        status=seller.status,
        user_is_active=user.is_active,
        user_is_verified=user.is_verified,
        created_at=seller.created_at,
    )


def _to_admin_product_detail(product: Product, seller_products: list[Product]) -> AdminProductDetailResponse:
    seller = product.__dict__.get("seller")
    user = seller.__dict__.get("user") if seller else None
    inventory = product.__dict__.get("inventory")
    images = product.__dict__.get("images") or []
    category = product.__dict__.get("category")
    brand = product.__dict__.get("brand")

    return AdminProductDetailResponse(
        id=product.id,
        name=product.name,
        slug=product.slug,
        description=product.description,
        sku=product.sku,
        price=product.price,
        compare_at_price=product.compare_at_price,
        status=product.status,
        category_id=product.category_id,
        category_name=category.name if category else None,
        brand_name=brand.name if brand else None,
        quantity_available=inventory.quantity_available if inventory else None,
        images=[
            AdminProductImageItem(
                id=img.id,
                url=img.url,
                alt_text=img.alt_text,
                sort_order=img.sort_order,
                is_primary=img.is_primary,
            )
            for img in sorted(images, key=lambda i: i.sort_order)
        ],
        created_at=product.created_at,
        updated_at=product.updated_at,
        seller=AdminSellerSummary(
            id=seller.id if seller else product.seller_id,
            store_name=seller.store_name if seller else "",
            store_slug=seller.store_slug if seller else "",
            status=seller.status if seller else "pending",
            description=seller.description if seller else None,
            email=user.email if user else "",
            full_name=user.full_name if user else None,
            joined_at=seller.created_at if seller else product.created_at,
        ),
        seller_products=[_to_admin_product(p) for p in seller_products],
    )


def _to_admin_product(product: Product) -> AdminProductItem:
    seller = product.__dict__.get("seller")
    inventory = product.__dict__.get("inventory")
    images = product.__dict__.get("images") or []
    category = product.__dict__.get("category")

    primary_image = next((img for img in images if img.is_primary), None) or (images[0] if images else None)

    return AdminProductItem(
        id=product.id,
        name=product.name,
        slug=product.slug,
        price=product.price,
        status=product.status,
        primary_image_url=primary_image.url if primary_image else None,
        category_name=category.name if category else None,
        seller_id=product.seller_id,
        store_name=seller.store_name if seller else "",
        store_slug=seller.store_slug if seller else "",
        quantity_available=inventory.quantity_available if inventory else None,
        created_at=product.created_at,
    )
