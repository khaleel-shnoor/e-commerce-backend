"""Aggregate all v1 API routers."""

from fastapi import APIRouter

from app.api.v1.routes import (
    admin,
    auth,
    categories,
    health,
    products,
    profile,
    seller_products,
    status,
)
from app.core.constants import API_V1_PREFIX

api_router = APIRouter(prefix=API_V1_PREFIX)
api_router.include_router(health.router)
api_router.include_router(status.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(admin.router)
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(seller_products.router)
