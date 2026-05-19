"""Database seed utilities — roles and demo data."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import RoleName
from app.models.user import Role
from app.repositories.user import RoleRepository


async def seed_roles(session: AsyncSession) -> None:
    """Ensure default RBAC roles exist."""
    repo = RoleRepository(session)
    for role_name in RoleName:
        existing = await repo.get_by_name(role_name)
        if existing is None:
            await repo.add(Role(name=role_name, description=f"{role_name.value} role"))
