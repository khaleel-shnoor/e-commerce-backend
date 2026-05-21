"""Customer-facing routes: cart, wishlist, orders, addresses."""

import uuid

from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DbSession
from app.models.enums import RoleName
from app.schemas.common import MessageResponse
from app.schemas.order import (
    AddressCreate,
    AddressListResponse,
    AddressResponse,
    CartAddRequest,
    CartResponse,
    CartUpdateRequest,
    CheckoutRequest,
    OrderDetailResponse,
    OrderListResponse,
    WishlistResponse,
    WishlistToggleResponse,
)
from app.services.order import OrderService

router = APIRouter(prefix="/customer", tags=["customer"])


def _svc(db: DbSession) -> OrderService:
    return OrderService(db)


# ── Wishlist ───────────────────────────────────────────────────────────────────

@router.get("/wishlist", response_model=WishlistResponse)
async def get_wishlist(user: CurrentUser, db: DbSession):
    return await _svc(db).get_wishlist(user.id)


@router.post("/wishlist/{product_id}", response_model=WishlistToggleResponse)
async def toggle_wishlist(product_id: uuid.UUID, user: CurrentUser, db: DbSession):
    return await _svc(db).toggle_wishlist(user.id, product_id)


# ── Cart ───────────────────────────────────────────────────────────────────────

@router.get("/cart", response_model=CartResponse)
async def get_cart(user: CurrentUser, db: DbSession):
    return await _svc(db).get_cart(user.id)


@router.post("/cart", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(req: CartAddRequest, user: CurrentUser, db: DbSession):
    return await _svc(db).add_to_cart(user.id, req)


@router.patch("/cart/{item_id}", response_model=CartResponse)
async def update_cart_item(item_id: uuid.UUID, req: CartUpdateRequest, user: CurrentUser, db: DbSession):
    return await _svc(db).update_cart_item(user.id, item_id, req.quantity)


@router.delete("/cart/{item_id}", response_model=CartResponse)
async def remove_cart_item(item_id: uuid.UUID, user: CurrentUser, db: DbSession):
    return await _svc(db).remove_from_cart(user.id, item_id)


@router.delete("/cart", response_model=CartResponse)
async def clear_cart(user: CurrentUser, db: DbSession):
    return await _svc(db).clear_cart(user.id)


# ── Addresses ──────────────────────────────────────────────────────────────────

@router.get("/addresses", response_model=AddressListResponse)
async def list_addresses(user: CurrentUser, db: DbSession):
    return await _svc(db).list_addresses(user.id)


@router.post("/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(req: AddressCreate, user: CurrentUser, db: DbSession):
    return await _svc(db).create_address(user.id, req)


@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: uuid.UUID, user: CurrentUser, db: DbSession):
    await _svc(db).delete_address(user.id, address_id)


# ── Orders ─────────────────────────────────────────────────────────────────────

@router.get("/orders", response_model=OrderListResponse)
async def list_orders(user: CurrentUser, db: DbSession):
    return await _svc(db).list_orders(user.id)


@router.get("/orders/{order_id}", response_model=OrderDetailResponse)
async def get_order(order_id: uuid.UUID, user: CurrentUser, db: DbSession):
    return await _svc(db).get_order(user.id, order_id)


@router.post("/orders/checkout", response_model=OrderDetailResponse, status_code=status.HTTP_201_CREATED)
async def checkout(req: CheckoutRequest, user: CurrentUser, db: DbSession):
    return await _svc(db).checkout(user.id, req)
