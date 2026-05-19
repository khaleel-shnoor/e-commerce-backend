"""User profile routes."""

from fastapi import APIRouter, File, UploadFile

from app.core.dependencies import CurrentUser, ProfileServiceDep
from app.schemas.auth import UserResponse
from app.schemas.profile import ProfileUpdateRequest

router = APIRouter(prefix="/users/me", tags=["profile"])


@router.get("", response_model=UserResponse)
async def get_my_profile(user: CurrentUser, profile: ProfileServiceDep) -> UserResponse:
    return await profile.get_profile(user)


@router.patch("", response_model=UserResponse)
async def update_my_profile(
    body: ProfileUpdateRequest,
    user: CurrentUser,
    profile: ProfileServiceDep,
) -> UserResponse:
    return await profile.update_profile(user, body)


@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    user: CurrentUser,
    profile: ProfileServiceDep,
    file: UploadFile = File(...),
) -> UserResponse:
    return await profile.upload_avatar(user, file)
