from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from ..models.post import Post
from ..schemas.post import PostCreate, PostUpdate
from ..utils.sanitizer import sanitize_html

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

async def get_post_by_id(db: AsyncSession, post_id: int):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post

async def generate_unique_slug(db: AsyncSession, base_slug: str, exclude_id: int = None):
    slug = base_slug
    counter = 1
    while True:
        existing = await get_posts_slug(db, slug)
        if not existing or (exclude_id and existing.id == exclude_id):
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1

async def create_post(db: AsyncSession, data: PostCreate):
    unique_slug = await generate_unique_slug(db, data.slug)
    data.slug = unique_slug
    if data.content_html:
        data.content_html = sanitize_html(data.content_html)
    post = Post(**data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def update_post(db: AsyncSession, post_id: int, data: PostUpdate):
    post = await get_post_by_id(db, post_id)
    if data.title is not None:
        post.title = data.title
    if data.slug is not None:
        unique_slug = await generate_unique_slug(db, data.slug, exclude_id=post_id)
        post.slug = unique_slug
    if data.content is not None:
        post.content = data.content
    if data.content_html is not None:
        post.content_html = sanitize_html(data.content_html)
    if data.category_id is not None:
        post.category_id = data.category_id
    await db.commit()
    await db.refresh(post)
    return post

async def delete_post(db: AsyncSession, post_id: int):
    post = await get_post_by_id(db, post_id)
    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully"}