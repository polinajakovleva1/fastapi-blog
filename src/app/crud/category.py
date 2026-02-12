from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.category import Category
from ..schemas.category import CategoryCreate

async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()

async def get_categories_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(Category).where(Category.slug==slug))
    return result.scalar_one_or_none()
