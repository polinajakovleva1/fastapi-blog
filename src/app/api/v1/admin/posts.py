from sqlalchemy.ext.asyncio import AsyncSession
from ....crud.post import get_post_by_id, create_post, update_post, delete_post, PostCreate, PostUpdate

async def get_post_id(db: AsyncSession, post_id: int):
    return await get_post_by_id(db, post_id)

async def create_new_post(db: AsyncSession, data: PostCreate):
    return await create_post(db, data)

async def update_existing_post(db: AsyncSession, post_id: int, data: PostUpdate):
    return await update_post(db, post_id, data)

async def delete_existing_post(db: AsyncSession, post_id: int):
    return await delete_post(db, post_id)