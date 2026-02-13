from sqlalchemy.ext.asyncio import AsyncSession
from ....crud.user import get_user_by_id, get_user_list, change_user_role

async def get_user(db: AsyncSession, user_id: int):
    return await get_user_by_id(db, user_id)

async def get_users(db: AsyncSession):
    return await get_user_list(db)

async def change_role(db: AsyncSession, user_id: int):
    return await change_user_role(db, user_id) 
