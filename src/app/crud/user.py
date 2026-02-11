from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User

async def create_test_users(db: AsyncSession):
    result = await db.execute(select(User))
    if not result.scalars().first():
        user_1 = User(email="email1@mail.com", hashed_password="1234")
        user_2 = User(email="email2@mail.com", hashed_password="5678")
        db.add_all([user_1, user_2])
        db.commit()

    result = await db.execute(select(User))
    return result.scalars().all()