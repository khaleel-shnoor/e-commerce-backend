"""User and role repositories."""

import uuid

from sqlalchemy import select
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
