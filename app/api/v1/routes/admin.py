"""Admin API routes — users, sellers, orders, and analytics."""

from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import AdminUser, DbSession
from app.models.enums import RoleName, SellerStatus
from app.schemas.admin import (
    AdminSellerItem,
    AdminSellersListResponse,
    AdminUsersListResponse,
    UpdateSellerStatusRequest,
)
from app.schemas.order import (
    AdminAnalyticsResponse,
    AdminOrderDetailResponse,
    AdminOrderListItem,
    AdminOrderListResponse,
    OrderDetailResponse,
    OrderListResponse,
    UpdateOrderStatusRequest,
)
from app.services.admin import AdminService
from app.services.order import OrderService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=AdminUsersListResponse)
async def list_users(
    _admin: AdminUser,
    db: DbSession,
    search: str | None = Query(default=None, max_length=255),
    role: RoleName | None = None,
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> AdminUsersListResponse:
    """List platform users (admin only)."""
    service = AdminService(db)
    items, total = await service.list_users(
        search=search,
        role=role,
        limit=limit,
        offset=offset,
    )
    return AdminUsersListResponse(items=items, total=total)


@router.get("/sellers", response_model=AdminSellersListResponse)
async def list_sellers(
    _admin: AdminUser,
    db: DbSession,
    search: str | None = Query(default=None, max_length=255),
    status: SellerStatus | None = None,
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> AdminSellersListResponse:
    """List seller profiles with linked user accounts (admin only)."""
    service = AdminService(db)
    items, total = await service.list_sellers(
        search=search,
        status=status,
        limit=limit,
        offset=offset,
    )
    return AdminSellersListResponse(items=items, total=total)


@router.patch("/sellers/{seller_id}/status", response_model=AdminSellerItem)
async def update_seller_status(
    seller_id: UUID,
    body: UpdateSellerStatusRequest,
    _admin: AdminUser,
    db: DbSession,
) -> AdminSellerItem:
    """Approve, reject, or suspend a seller account (admin only)."""
    service = AdminService(db)
    return await service.update_seller_status(seller_id, status=body.status)


@router.get("/analytics", response_model=AdminAnalyticsResponse)
async def get_admin_analytics(_admin: AdminUser, db: DbSession) -> AdminAnalyticsResponse:
    """Platform-wide analytics (admin only)."""
    svc = OrderService(db)
    return await svc.get_admin_analytics()


@router.get("/orders", response_model=AdminOrderListResponse)
async def list_all_orders(
    _admin: AdminUser,
    db: DbSession,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> AdminOrderListResponse:
    """List all platform orders (admin only)."""
    from sqlalchemy import func, select
    from sqlalchemy.orm import selectinload
    from app.models.order import Order, OrderItem

    stmt = (
        select(Order)
        .options(selectinload(Order.items), selectinload(Order.user))
        .order_by(Order.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.scalars(stmt)
    orders = list(result.unique().all())

    count_stmt = select(func.count()).select_from(Order)
    total = int((await db.scalar(count_stmt)) or 0)

    return AdminOrderListResponse(
        items=[
            AdminOrderListItem(
                id=o.id,
                order_number=o.order_number,
                status=o.status,
                total_amount=o.total_amount,
                item_count=len(o.items),
                created_at=o.created_at,
                buyer_name=o.user.full_name if o.user else None,
                buyer_email=o.user.email if o.user else "",
            )
            for o in orders
        ],
        total=total,
    )


@router.get("/orders/{order_id}", response_model=AdminOrderDetailResponse)
async def get_order_detail(
    order_id: UUID,
    _admin: AdminUser,
    db: DbSession,
) -> AdminOrderDetailResponse:
    """Get full order detail including buyer and seller info (admin only)."""
    svc = OrderService(db)
    return await svc.get_admin_order_detail(order_id)


@router.patch("/orders/{order_id}/status", response_model=AdminOrderDetailResponse)
async def update_order_status(
    order_id: UUID,
    body: UpdateOrderStatusRequest,
    _admin: AdminUser,
    db: DbSession,
) -> AdminOrderDetailResponse:
    """Update the status of an order (admin only)."""
    svc = OrderService(db)
    return await svc.update_order_status(order_id, body.status)
