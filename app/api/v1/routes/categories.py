"""Public category routes."""

from fastapi import APIRouter

from app.core.dependencies import ProductServiceDep
from app.schemas.product import CategoryListResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=CategoryListResponse)
async def list_categories(service: ProductServiceDep) -> CategoryListResponse:
    """List active product categories."""
    return await service.list_categories()
