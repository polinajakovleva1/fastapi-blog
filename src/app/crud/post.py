from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.post import Post
from ..schemas.post import PostCreate

async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars().all()

async def get_posts_slug(db: AsyncSession, slug: str):
    post = select(Post).where(Post.slug==slug)
    result = await db.execute(post)
    return result.scalar_one_or_none()

async def get_posts_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Post).where(Post.category_id==category_id))
    return result.scalars().all()