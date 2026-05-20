"""Public product catalog routes."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import ProductServiceDep
from app.schemas.product import ProductDetailResponse, ProductListResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
async def list_products(
    service: ProductServiceDep,
    search: str | None = Query(default=None, max_length=255),
    category_id: UUID | None = None,
    seller_id: UUID | None = None,
    min_price: Decimal | None = Query(default=None, ge=0),
    max_price: Decimal | None = Query(default=None, ge=0),
    sort: str = Query(default="newest", pattern="^(newest|price-asc|price-desc|name)$"),
    limit: int = Query(default=24, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ProductListResponse:
    """List active products from approved sellers (customer shop)."""
    return await service.list_public(
        search=search,
        category_id=category_id,
        seller_id=seller_id,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@router.get("/{identifier}", response_model=ProductDetailResponse)
async def get_product(identifier: str, service: ProductServiceDep) -> ProductDetailResponse:
    """Product detail by UUID or slug (active listings only)."""
    return await service.get_public(identifier)
