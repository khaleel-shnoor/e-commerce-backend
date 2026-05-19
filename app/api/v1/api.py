"""Aggregate all v1 API routers."""

from fastapi import APIRouter

from app.api.v1.routes import auth, health, profile, status
from app.core.constants import API_V1_PREFIX

api_router = APIRouter(prefix=API_V1_PREFIX)
api_router.include_router(health.router)
api_router.include_router(status.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
