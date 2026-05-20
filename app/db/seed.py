"""Database seed utilities — roles and demo data."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Category
from app.models.enums import RoleName
from app.models.user import Role
from app.repositories.category import CategoryRepository
from app.repositories.user import RoleRepository
from app.utils.slug import slugify

DEFAULT_CATEGORIES = [
    ("Apparel", "apparel"),
    ("Footwear", "footwear"),
    ("Accessories", "accessories"),
    ("Outerwear", "outerwear"),
]


async def seed_roles(session: AsyncSession) -> None:
    """Ensure default RBAC roles exist."""
    repo = RoleRepository(session)
    for role_name in RoleName:
        existing = await repo.get_by_name(role_name)
        if existing is None:
            await repo.add(Role(name=role_name, description=f"{role_name.value} role"))


async def seed_categories(session: AsyncSession) -> None:
    """Ensure default shop categories exist."""
    repo = CategoryRepository(session)
    for name, slug in DEFAULT_CATEGORIES:
        existing = await repo.get_by_slug(slug)
        if existing is None:
            await repo.add(
                Category(
                    name=name,
                    slug=slug,
                    description=f"{name} collection",
                    is_active=True,
                )
            )
