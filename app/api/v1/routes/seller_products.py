"""Seller product management routes."""

from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status

from app.core.dependencies import CurrentUser, ProductServiceDep, require_roles
from app.core.exceptions import ValidationError
from app.models.enums import ProductStatus, RoleName
from app.schemas.common import MessageResponse
from app.schemas.product import (
    ProductCreateRequest,
    ProductDetailResponse,
    ProductListResponse,
    ProductUpdateRequest,
)

router = APIRouter(
    prefix="/seller/products",
    tags=["seller-products"],
    dependencies=[Depends(require_roles(RoleName.SELLER))],
)


def _optional_uuid(value: str | None) -> UUID | None:
    if value is None or value == "":
        return None
    try:
        return UUID(value)
    except ValueError as exc:
        raise ValidationError("Invalid category id") from exc


@router.get("", response_model=ProductListResponse)
async def list_my_products(
    user: CurrentUser,
    service: ProductServiceDep,
    search: str | None = Query(default=None, max_length=255),
    status: ProductStatus | None = None,
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> ProductListResponse:
    """List products for the authenticated approved seller."""
    return await service.list_for_seller(
        user.id,
        search=search,
        status=status,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ProductDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    user: CurrentUser,
    service: ProductServiceDep,
    name: Annotated[str, Form()],
    price: Annotated[Decimal, Form(gt=0)],
    description: Annotated[str | None, Form()] = None,
    sku: Annotated[str | None, Form()] = None,
    compare_at_price: Annotated[Decimal | None, Form(gt=0)] = None,
    category_id: Annotated[str | None, Form()] = None,
    brand_id: Annotated[str | None, Form()] = None,
    status_value: Annotated[ProductStatus, Form(alias="status")] = ProductStatus.DRAFT,
    quantity_available: Annotated[int, Form(ge=0)] = 0,
    image: Annotated[UploadFile | None, File()] = None,
) -> ProductDetailResponse:
    """Create a product with optional image upload (Cloudinary)."""
    body = ProductCreateRequest(
        name=name,
        description=description,
        sku=sku,
        price=price,
        compare_at_price=compare_at_price,
        category_id=_optional_uuid(category_id),
        brand_id=_optional_uuid(brand_id),
        status=status_value,
        quantity_available=quantity_available,
    )
    return await service.create_for_seller(user.id, body, image_file=image)


@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_my_product(
    product_id: UUID,
    user: CurrentUser,
    service: ProductServiceDep,
) -> ProductDetailResponse:
    return await service.get_for_seller(user.id, product_id)


@router.patch("/{product_id}", response_model=ProductDetailResponse)
async def update_product(
    product_id: UUID,
    user: CurrentUser,
    service: ProductServiceDep,
    name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    sku: Annotated[str | None, Form()] = None,
    price: Annotated[Decimal | None, Form(gt=0)] = None,
    compare_at_price: Annotated[Decimal | None, Form()] = None,
    category_id: Annotated[str | None, Form()] = None,
    brand_id: Annotated[str | None, Form()] = None,
    status_value: Annotated[ProductStatus | None, Form(alias="status")] = None,
    quantity_available: Annotated[int | None, Form(ge=0)] = None,
    image: Annotated[UploadFile | None, File()] = None,
) -> ProductDetailResponse:
    """Update product fields and/or replace the primary image."""
    fields_set = 0
    payload: dict = {}

    if name is not None:
        payload["name"] = name
        fields_set += 1
    if description is not None:
        payload["description"] = description
        fields_set += 1
    if sku is not None:
        payload["sku"] = sku
        fields_set += 1
    if price is not None:
        payload["price"] = price
        fields_set += 1
    if compare_at_price is not None:
        payload["compare_at_price"] = compare_at_price if compare_at_price > 0 else None
        fields_set += 1
    if category_id is not None:
        payload["category_id"] = _optional_uuid(category_id)
        fields_set += 1
    if brand_id is not None:
        payload["brand_id"] = _optional_uuid(brand_id)
        fields_set += 1
    if status_value is not None:
        payload["status"] = status_value
        fields_set += 1
    if quantity_available is not None:
        payload["quantity_available"] = quantity_available
        fields_set += 1

    if fields_set == 0 and image is None:
        raise ValidationError("No fields to update")

    body = ProductUpdateRequest(**payload)
    return await service.update_for_seller(
        user.id,
        product_id,
        body,
        image_file=image,
    )


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: UUID,
    user: CurrentUser,
    service: ProductServiceDep,
) -> MessageResponse:
    await service.delete_for_seller(user.id, product_id)
    return MessageResponse(message="Product deleted")
