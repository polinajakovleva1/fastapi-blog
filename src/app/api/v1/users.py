from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...crud.user import get_user
from ...core.dependencies import get_current

async def get_current_user(db: AsyncSession, token: str):
    email = await get_current(token)
    user = await get_user(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user