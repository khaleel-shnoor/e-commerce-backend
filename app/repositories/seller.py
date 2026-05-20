"""Seller repository."""

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import SellerStatus
from app.models.seller import Seller
from app.models.user import User
from app.repositories.base import BaseRepository


class SellerRepository(BaseRepository[Seller]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Seller)

    async def get_by_user_id(self, user_id) -> Seller | None:
        stmt = (
            select(Seller)
            .where(Seller.user_id == user_id)
            .options(selectinload(Seller.user).selectinload(User.roles))
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_id_with_user(self, seller_id) -> Seller | None:
        stmt = (
            select(Seller)
            .where(Seller.id == seller_id)
            .options(selectinload(Seller.user).selectinload(User.roles))
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def slug_exists(self, slug: str) -> bool:
        stmt = select(Seller.id).where(Seller.store_slug == slug).limit(1)
        result = await self.session.scalars(stmt)
        return result.first() is not None

    async def list_with_users(
        self,
        *,
        search: str | None = None,
        status: SellerStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Seller]:
        stmt = (
            select(Seller)
            .join(User, Seller.user_id == User.id)
            .options(selectinload(Seller.user).selectinload(User.roles))
            .order_by(Seller.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    User.email.ilike(term),
                    User.full_name.ilike(term),
                    Seller.store_name.ilike(term),
                    Seller.store_slug.ilike(term),
                )
            )
        if status is not None:
            stmt = stmt.where(Seller.status == status)
        result = await self.session.scalars(stmt)
        return list(result.unique().all())
