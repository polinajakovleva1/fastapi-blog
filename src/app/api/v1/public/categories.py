from sqlalchemy.ext.asyncio import AsyncSession
from ....crud.category import get_categories, get_categories_slug
from ....crud.post import get_posts_category

async def get_categories_list(db: AsyncSession):
    return await get_categories(db)

async def get_category(db: AsyncSession, slug: str):
    category = await get_categories_slug(db, slug)
    if not category:
        return []
    return await get_posts_category(db, category.id)


