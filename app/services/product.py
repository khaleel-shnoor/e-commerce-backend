"""Product catalog business logic."""

import uuid
from decimal import Decimal

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from app.models.catalog import Product, ProductImage
from app.models.enums import ProductStatus, SellerStatus
from app.models.inventory import Inventory
from app.models.seller import Seller
from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository
from app.repositories.seller import SellerRepository
from app.schemas.product import (
    CategoryListResponse,
    CategoryResponse,
    ProductCreateRequest,
    ProductDetailResponse,
    ProductImageResponse,
    ProductListItem,
    ProductListResponse,
    ProductUpdateRequest,
)
from app.services.cloudinary_storage import (
    ALLOWED_CONTENT_TYPES,
    MAX_PRODUCT_IMAGE_BYTES,
    CloudinaryStorage,
)
from app.utils.slug import slugify, unique_store_slug


class ProductService:
    def __init__(self, session: AsyncSession, settings: Settings | None = None) -> None:
        self.session = session
        self.settings = settings
        self.products = ProductRepository(session)
        self.categories = CategoryRepository(session)
        self.sellers = SellerRepository(session)
        self.storage = CloudinaryStorage(settings) if settings else None

    async def _require_approved_seller(self, user_id: uuid.UUID) -> Seller:
        seller = await self.sellers.get_by_user_id(user_id)
        if seller is None:
            raise AuthorizationError("Seller profile not found")
        if seller.status != SellerStatus.APPROVED:
            raise AuthorizationError(
                "Seller account must be approved before managing products"
            )
        user = seller.__dict__.get("user")
        if user is None or not user.is_verified:
            raise AuthorizationError("Verify your email before managing products")
        return seller

    async def _validate_category(self, category_id: uuid.UUID | None) -> None:
        if category_id is None:
            return
        category = await self.categories.get_by_id(category_id)
        if category is None or not category.is_active:
            raise ValidationError("Invalid or inactive category")

    async def _upload_product_image_file(
        self,
        file: UploadFile,
        *,
        seller_id: uuid.UUID,
        product_id: uuid.UUID,
    ) -> str:
        if self.storage is None or not self.storage.is_configured:
            raise ValidationError(
                "Image upload is not configured. Set CLOUDINARY_* variables in .env"
            )

        content_type = file.content_type or ""
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError("Allowed image formats: JPEG, PNG, WebP, GIF")

        file_bytes = await file.read()
        if not file_bytes:
            raise ValidationError("Empty image file")
        if len(file_bytes) > MAX_PRODUCT_IMAGE_BYTES:
            raise ValidationError("Image must be 10 MB or smaller")

        return await self.storage.upload_product_image(
            file_bytes,
            seller_id=str(seller_id),
            product_id=str(product_id),
        )

    async def _set_primary_image(
        self,
        product: Product,
        url: str,
        alt_text: str | None = None,
    ) -> None:
        """Set or replace primary image without lazy-loading relationships."""
        label = alt_text or product.name
        stmt = (
            select(ProductImage)
            .where(ProductImage.product_id == product.id)
            .order_by(ProductImage.sort_order)
            .limit(1)
        )
        result = await self.session.scalars(stmt)
        existing = result.first()
        if existing is not None:
            existing.url = url
            existing.alt_text = label
            existing.is_primary = True
        else:
            await self.products.add_image(
                ProductImage(
                    product_id=product.id,
                    url=url,
                    alt_text=label,
                    sort_order=0,
                    is_primary=True,
                )
            )

    def _primary_image_url(self, product: Product) -> str | None:
        images = product.__dict__.get("images")
        if not images:
            return None
        primary = next((img for img in images if img.is_primary), None)
        return (primary or images[0]).url

    def _to_list_item(self, product: Product) -> ProductListItem:
        inv = product.__dict__.get("inventory")
        qty = inv.quantity_available if inv is not None else None
        category = product.__dict__.get("category")
        brand = product.__dict__.get("brand")
        seller = product.__dict__.get("seller")
        return ProductListItem(
            id=product.id,
            slug=product.slug,
            name=product.name,
            price=product.price,
            compare_at_price=product.compare_at_price,
            status=product.status,
            primary_image_url=self._primary_image_url(product),
            category_id=product.category_id,
            category_name=category.name if category is not None else None,
            brand_name=brand.name if brand is not None else None,
            store_name=seller.store_name if seller is not None else None,
            quantity_available=qty,
        )

    def _to_detail(self, product: Product) -> ProductDetailResponse:
        base = self._to_list_item(product)
        images = product.__dict__.get("images") or []
        return ProductDetailResponse(
            **base.model_dump(),
            description=product.description,
            sku=product.sku,
            seller_id=product.seller_id,
            brand_id=product.brand_id,
            images=[
                ProductImageResponse(
                    id=img.id,
                    url=img.url,
                    alt_text=img.alt_text,
                    sort_order=img.sort_order,
                    is_primary=img.is_primary,
                )
                for img in images
            ],
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    async def list_categories(self) -> CategoryListResponse:
        rows = await self.categories.list_active()
        return CategoryListResponse(
            items=[
                CategoryResponse(
                    id=c.id,
                    name=c.name,
                    slug=c.slug,
                    description=c.description,
                    parent_id=c.parent_id,
                )
                for c in rows
            ]
        )

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
    ) -> ProductListResponse:
        rows = await self.products.list_public(
            search=search,
            category_id=category_id,
            seller_id=seller_id,
            min_price=min_price,
            max_price=max_price,
            sort=sort,
            limit=limit,
            offset=offset,
        )
        total = await self.products.count_public(
            search=search,
            category_id=category_id,
            seller_id=seller_id,
            min_price=min_price,
            max_price=max_price,
        )
        return ProductListResponse(
            items=[self._to_list_item(p) for p in rows],
            total=total,
        )

    async def get_public(self, identifier: str) -> ProductDetailResponse:
        product = None
        try:
            product_id = uuid.UUID(identifier)
            product = await self.products.get_public_by_id(product_id)
        except ValueError:
            product = await self.products.get_public_by_slug(identifier)
        if product is None:
            raise NotFoundError("Product not found")
        return self._to_detail(product)

    async def list_for_seller(
        self,
        user_id: uuid.UUID,
        *,
        search: str | None = None,
        status: ProductStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> ProductListResponse:
        seller = await self._require_approved_seller(user_id)
        rows = await self.products.list_for_seller(
            seller.id,
            search=search,
            status=status,
            limit=limit,
            offset=offset,
        )
        total = await self.products.count_for_seller(
            seller.id,
            search=search,
            status=status,
        )
        return ProductListResponse(
            items=[self._to_list_item(p) for p in rows],
            total=total,
        )

    async def get_for_seller(self, user_id: uuid.UUID, product_id: uuid.UUID) -> ProductDetailResponse:
        seller = await self._require_approved_seller(user_id)
        product = await self.products.get_by_id(product_id)
        if product is None or product.seller_id != seller.id:
            raise NotFoundError("Product not found")
        return self._to_detail(product)

    async def create_for_seller(
        self,
        user_id: uuid.UUID,
        data: ProductCreateRequest,
        *,
        image_file: UploadFile | None = None,
    ) -> ProductDetailResponse:
        seller = await self._require_approved_seller(user_id)
        await self._validate_category(data.category_id)

        base_slug = slugify(data.name)
        slug = await unique_store_slug(
            self.session,
            base_slug,
            exists=lambda s: self.products.slug_exists_for_seller(seller.id, s),
        )

        product = Product(
            seller_id=seller.id,
            category_id=data.category_id,
            brand_id=data.brand_id,
            name=data.name.strip(),
            slug=slug,
            description=data.description,
            sku=data.sku,
            price=data.price,
            compare_at_price=data.compare_at_price,
            status=data.status,
        )
        await self.products.add(product)

        await self.products.add_inventory(
            Inventory(
                product_id=product.id,
                quantity_available=data.quantity_available,
                quantity_reserved=0,
            )
        )

        if image_file is not None:
            url = await self._upload_product_image_file(
                image_file,
                seller_id=seller.id,
                product_id=product.id,
            )
            await self._set_primary_image(product, url, data.image_alt or data.name)
        elif data.image_url:
            await self._set_primary_image(
                product,
                data.image_url.strip(),
                data.image_alt or data.name,
            )

        product = await self.products.get_by_id(product.id)
        assert product is not None
        return self._to_detail(product)

    async def update_for_seller(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        data: ProductUpdateRequest,
        *,
        image_file: UploadFile | None = None,
    ) -> ProductDetailResponse:
        seller = await self._require_approved_seller(user_id)
        product = await self.products.get_by_id(product_id)
        if product is None or product.seller_id != seller.id:
            raise NotFoundError("Product not found")

        if data.category_id is not None:
            await self._validate_category(data.category_id)

        updates = data.model_dump(exclude_unset=True)
        image_url = updates.pop("image_url", None)
        image_alt = updates.pop("image_alt", None)
        quantity_available = updates.pop("quantity_available", None)

        for field, value in updates.items():
            setattr(product, field, value)

        if quantity_available is not None:
            if product.inventory is None:
                await self.products.add_inventory(
                    Inventory(
                        product_id=product.id,
                        quantity_available=quantity_available,
                        quantity_reserved=0,
                    )
                )
            else:
                product.inventory.quantity_available = quantity_available

        if image_file is not None:
            url = await self._upload_product_image_file(
                image_file,
                seller_id=seller.id,
                product_id=product.id,
            )
            await self._set_primary_image(product, url, image_alt or product.name)
        elif image_url:
            await self._set_primary_image(
                product,
                image_url.strip(),
                image_alt or product.name,
            )

        await self.session.flush()
        product = await self.products.get_by_id(product.id)
        assert product is not None
        return self._to_detail(product)

    async def delete_for_seller(self, user_id: uuid.UUID, product_id: uuid.UUID) -> None:
        seller = await self._require_approved_seller(user_id)
        product = await self.products.get_by_id(product_id)
        if product is None or product.seller_id != seller.id:
            raise NotFoundError("Product not found")
        await self.products.delete(product)
