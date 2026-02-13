from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..models.user import User
from sqlalchemy import select
from ..core.security import get_password_hash

async def create_user(db: AsyncSession, email: str, password: str):
    """Создание объекта класса User"""
    hashed_pass = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_pass)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, email: str):
    """Получение объекта класса User с указанным email"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int):
    """Получение объекта класса User с указанным id"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

async def get_user_list(db: AsyncSession):
    """Получение всех объектов класса User"""
    result = await db.execute(select(User))
    return result.scalars().all()

async def change_user_role(db: AsyncSession, user_id: int):
    """Изменение роли пользователя"""
    user = await get_user_by_id(db, user_id)
    user.role = "ADMIN" if user.role == "USER" else "USER"
    await db.commit()
    await db.refresh(user)
    return user
