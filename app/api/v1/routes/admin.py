"""Admin API routes — users and sellers."""

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
from app.services.admin import AdminService

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
