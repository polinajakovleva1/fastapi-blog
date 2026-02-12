from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from sqlalchemy import select
from ..core.security import get_password_hash

async def create_user(db: AsyncSession, email: str, password: str):
    hashed_pass = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_pass)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
