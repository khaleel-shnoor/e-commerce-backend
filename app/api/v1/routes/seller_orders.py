"""Seller order management and analytics routes."""

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.core.exceptions import AuthorizationError
from app.models.enums import RoleName, SellerStatus
from app.repositories.seller import SellerRepository
from app.schemas.order import SellerAnalyticsResponse, SellerOrderListResponse
from app.services.order import OrderService

router = APIRouter(
    prefix="/seller",
    tags=["seller-orders"],
    dependencies=[Depends(require_roles(RoleName.SELLER))],
)


async def _get_approved_seller(user: CurrentUser, db: DbSession):
    repo = SellerRepository(db)
    seller = await repo.get_by_user_id(user.id)
    if seller is None or seller.status != SellerStatus.APPROVED:
        raise AuthorizationError("Seller account must be approved")
    return seller


@router.get("/orders", response_model=SellerOrderListResponse)
async def list_seller_orders(
    user: CurrentUser,
    db: DbSession,
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
) -> SellerOrderListResponse:
    """List orders containing this seller's products."""
    seller = await _get_approved_seller(user, db)
    svc = OrderService(db)
    return await svc.list_seller_orders(seller.id, limit=limit, offset=offset)


@router.get("/analytics", response_model=SellerAnalyticsResponse)
async def get_seller_analytics(user: CurrentUser, db: DbSession) -> SellerAnalyticsResponse:
    """Seller dashboard analytics."""
    seller = await _get_approved_seller(user, db)
    svc = OrderService(db)
    return await svc.get_seller_analytics(seller.id)
