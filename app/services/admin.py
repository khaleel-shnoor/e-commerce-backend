"""Admin panel business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import RoleName, SellerStatus
from app.models.seller import Seller
from app.models.user import User
from app.repositories.seller import SellerRepository
from app.repositories.user import UserRepository
from app.schemas.admin import AdminSellerItem, AdminUserItem


class AdminService:
    """List and manage platform users and sellers."""

    def __init__(self, session: AsyncSession) -> None:
        self.users = UserRepository(session)
        self.sellers = SellerRepository(session)

    async def list_users(
        self,
        *,
        search: str | None = None,
        role: RoleName | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AdminUserItem], int]:
        rows = await self.users.list_with_roles(
            search=search,
            role=role,
            limit=limit,
            offset=offset,
        )
        return [_to_admin_user(u) for u in rows], len(rows)

    async def list_sellers(
        self,
        *,
        search: str | None = None,
        status: SellerStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AdminSellerItem], int]:
        rows = await self.sellers.list_with_users(
            search=search,
            status=status,
            limit=limit,
            offset=offset,
        )
        return [_to_admin_seller(s) for s in rows], len(rows)


def _to_admin_user(user: User) -> AdminUserItem:
    return AdminUserItem(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        roles=[r.name.value for r in user.roles],
        is_active=user.is_active,
        is_verified=user.is_verified,
        has_password=user.password_hash is not None,
        created_at=user.created_at,
    )


def _to_admin_seller(seller: Seller) -> AdminSellerItem:
    user = seller.user
    return AdminSellerItem(
        id=seller.id,
        user_id=seller.user_id,
        email=user.email,
        full_name=user.full_name,
        store_name=seller.store_name,
        store_slug=seller.store_slug,
        status=seller.status,
        user_is_active=user.is_active,
        created_at=seller.created_at,
    )
