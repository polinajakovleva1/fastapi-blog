from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..core.database import get_db
from ..schemas.category import CategoryPublic
from ..schemas.post import PostPublic
from .v1.auth import register_user, login_user, refr_token
from .v1.users import get_current_user
from .v1.public.categories import get_categories_list, get_category
from .v1.public.posts import get_posts_list, get_post_slug 

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

@router.get("/categories", response_model=list[CategoryPublic])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    return await get_categories_list(db)

@router.get("/categories/{slug}/posts", response_model=list[PostPublic])
async def get_category_posts(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_category(db, slug)

@router.get("/posts", response_model=list[PostPublic])
async def get_posts(
    db: AsyncSession = Depends(get_db)
):
    return await get_posts_list(db)

@router.get("/posts/{slug}", response_model=PostPublic)
async def get_post(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_post_slug(db, slug)