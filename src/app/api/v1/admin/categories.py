from sqlalchemy.ext.asyncio import AsyncSession
from ....crud.category import get_category_by_id, create_category, update_category, delete_category, CategoryCreate, CategoryUpdate

async def get_category_id(db: AsyncSession, category_id: int):
    return await get_category_by_id(db, category_id)

async def create_new_category(db: AsyncSession, data: CategoryCreate):
    return await create_category(db, data)

async def update_existing_category(db: AsyncSession, category_id: int, data: CategoryUpdate):
    return await update_category(db, category_id, data)

async def delete_existing_category(db: AsyncSession, category_id: int):
    return await delete_category(db, category_id)