from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..core.database import get_db
from .v1.auth import register_user, login_user, refr_token
from .v1.users import get_current_user

router = APIRouter(prefix="/api/v1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


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

@router.get("/users/me")
async def users_me(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return await get_current_user(db, token)