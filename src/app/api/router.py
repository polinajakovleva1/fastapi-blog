from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..core.database import get_db
from .v1.auth import register_user, login_user, refr_token

router = APIRouter(prefix="/api/v1")

@router.post("/auth/register")
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await register_user(form_data, db)

@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await login_user(form_data, db)

@router.post("/auth/refresh")
async def refresh(
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    return await refr_token(refresh_token, db)