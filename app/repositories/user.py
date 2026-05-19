"""User and role repositories."""

import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import RoleName
from app.models.user import Role, User, UserRole
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email.lower())
            .options(selectinload(User.roles))
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_with_roles(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id).options(selectinload(User.roles))
        result = await self.session.scalars(stmt)
        return result.first()

    async def list_with_roles(
        self,
        *,
        search: str | None = None,
        role: RoleName | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[User]:
        stmt = select(User).options(selectinload(User.roles)).order_by(User.created_at.desc())

        if role is not None:
            stmt = stmt.join(User.roles).where(Role.name == role)

        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    User.email.ilike(term),
                    User.full_name.ilike(term),
                    User.phone.ilike(term),
                )
            )

        stmt = stmt.distinct().limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return list(result.all())


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Role)

    async def get_by_name(self, name: RoleName) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        result = await self.session.scalars(stmt)
        return result.first()

    async def assign_role(self, user: User, role: Role) -> None:
        existing = await self.session.get(
            UserRole,
            {"user_id": user.id, "role_id": role.id},
        )
        if existing is None:
            self.session.add(UserRole(user_id=user.id, role_id=role.id))
            await self.session.flush()
