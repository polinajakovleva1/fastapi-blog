from sqlalchemy.ext.asyncio import AsyncSession
from ....crud.post import get_posts, get_posts_slug

async def get_posts_list(db: AsyncSession):
    return await get_posts(db)

async def get_post_slug(db: AsyncSession, slug: str):
    return await get_posts_slug(db, slug)

