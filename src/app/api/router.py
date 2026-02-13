from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..core.database import get_db
from ..core.dependencies import require_admin
from ..schemas.category import CategoryPublic, CategoryAdmin
from ..schemas.post import PostPublic, PostAdmin
from .v1.auth import register_user, login_user, refr_token
from .v1.users import get_me, User
from .v1.public.categories import get_categories_list, get_category
from .v1.public.posts import get_posts_list, get_post_slug
from .v1.admin.users import get_user, get_users, change_role 
from .v1.admin.categories import get_category_id, create_new_category, update_existing_category, delete_existing_category, CategoryCreate, CategoryUpdate
from .v1.admin.posts import get_post_id, create_new_post, update_existing_post, delete_existing_post, PostCreate, PostUpdate

router = APIRouter(prefix="/api/v1")

@router.post("/auth/register")
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация пользователя

    принимает: 
        email (username в form-data)
        password

    возвращает
        access_token
        refresh_token
        token_type: bearer
    """
    return await register_user(form_data, db)

@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация пользователя

    принимает: 
        email (username в form-data)
        password

    возвращает:
        access_token
        refresh_token
        token_type: bearer
    """
    return await login_user(form_data, db)

@router.post("/auth/refresh")
async def refresh(
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление токенов

    принимает:
        refresh_token (в теле запроса)

    возвращает:
        access_token
        refresh_token
        token_type: bearer
    """
    return await refr_token(refresh_token, db)

@router.get("/users/me")
async def users_me(
    current_user: User = Depends(get_me) 
):
    """
    Текущий пользователь

    требует:
        access_token в заголовке Authorization

    возвращает:
        email
        role
    """
    return current_user

@router.get("/categories", response_model=list[CategoryPublic])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    Список всех категорий

    публичный доступ

    возвращает массив категорий с полями:
        name
        slug
    """
    return await get_categories_list(db)

@router.get("/categories/{slug}/posts", response_model=list[PostPublic])
async def get_category_posts(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Список постов конкретной категории
    
    публичный доступ

    принимает slug категории

    возвращает массив постов с полями:
        title
        slug
        content
        content_html
        created_at
        updated_at
        author (объект класса UserPublic)
        category (объект класса CategoryPublic)
    """
    return await get_category(db, slug)

@router.get("/posts", response_model=list[PostPublic])
async def get_posts(
    db: AsyncSession = Depends(get_db)
):
    """
    Список всех постов

    публичный доступ

    возвращает массив постов с полями:
        title
        slug
        content
        content_html
        created_at
        updated_at
        author (объект класса UserPublic)
        category (объект класса CategoryPublic)
    """
    return await get_posts_list(db)

@router.get("/posts/{slug}", response_model=PostPublic)
async def get_post(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение поста по slug

    публичный доступ
    
    принимает slug поста

    возвращает пост с полями:
        title
        slug
        content
        content_html
        created_at
        updated_at
        author (объект класса UserPublic)
        category (объект класса CategoryPublic)
    """
    return await get_post_slug(db, slug)

@router.get("/admin/users", dependencies=[Depends(require_admin)])
async def get_admin_users(
    db: AsyncSession = Depends(get_db)
):
    """
    Список пользователей

    доступно только ADMIN

    возвращает массив пользователей с полями:
        id
        email
        role
        created_at
    """
    return await get_users(db)

@router.get("/admin/users/{user_id}", dependencies=[Depends(require_admin)])
async def get_admin_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение пользователя по id

    доступно только ADMIN

    принимает id пользователя

    возвращает:
        id
        email
        role
        created_at
    """
    return await get_user(db, user_id)

@router.patch("/admin/users/{user_id}/role", dependencies=[Depends(require_admin)]
)
async def change_user_role(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Изменение роли пользователя

    доступно только ADMIN

    принимает id пользователя

    меняет роль ADMIN на USER и наоборот

    возвращает:
        id
        email
        role
        created_at
    """
    return await change_role(db, user_id)

@router.get("/admin/categories", dependencies=[Depends(require_admin)])
async def get_admin_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    Список всех категорий

    доступно только ADMIN

    возвращает массив категорий с полями:
        id
        name
        slug
        created_at
    """
    return await get_categories_list(db)

@router.get("/admin/categories/{category_id}", dependencies=[Depends(require_admin)])
async def get_admin_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение категории по id

    доступно только ADMIN

    принимает id категории

    возвращает:
        id
        name
        slug
        created_at
    """
    return await get_category_id(db, category_id)

@router.post("/admin/categories", dependencies=[Depends(require_admin)])
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создание новой категории

    доступно только ADMIN

    принимает name название категории и slug опционально (генерируется автоматически)

    возвращает:
        id
        name
        slug
        created_at
    """
    return await create_new_category(db, data)

@router.patch("/admin/categories/{category_id}", dependencies=[Depends(require_admin)])
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление категории

    доступно только ADMIN

    принимает id категории, name новвое название категории и slug опционально (генерируется автоматически)

    возвращает:
        id
        name
        slug
        created_at
    """
    return await update_existing_category(db, category_id, data)

@router.delete("/admin/categories/{category_id}", dependencies=[Depends(require_admin)])
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Удаление категории

    доступно только ADMIN

    принимает id категории

    также удаляет все посты в категории

    возвращает confirmation message
    """
    return await delete_existing_category(db, category_id)

@router.get("/admin/posts", response_model=list[PostAdmin], dependencies=[Depends(require_admin)])
async def get_admin_posts_list(
    db: AsyncSession = Depends(get_db)
):
    """
    Список всех постов

    доступно только ADMIN

    возвращает массив постов с полями:
        id
        title
        slug
        content: str
        content_html
        created_at
        updated_at
        author_id
        category_id
        author (объект класса UserAdmin)
        category (объект класса CategoryAdmin)
    """
    return await get_posts_list(db)

@router.get("/admin/posts/{post_id}", response_model=PostAdmin, dependencies=[Depends(require_admin)])
async def get_admin_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение поста по id

    доступно только ADMIN

    возвращает:
        id
        title
        slug
        content: str
        content_html
        created_at
        updated_at
        author_id
        category_id
        author (объект класса UserAdmin)
        category (объект класса CategoryAdmin)
    """
    return await get_post_id(db, post_id)

@router.post("/admin/posts", response_model=PostAdmin, dependencies=[Depends(require_admin)])
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создание поста

    доступно только ADMIN

    принимает:
        title: заголовок
        content: текст
        content_html: HTML версия (опционально)
        category_id: id категории
        author_id: id автора
        slug: опционально (генерируется из title)

    HTML очищается от XSS через bleach

    возвращает:
        id
        title
        slug
        content: str
        content_html
        created_at
        updated_at
        author_id
        category_id
        author (объект класса UserAdmin)
        category (объект класса CategoryAdmin)
    """
    return await create_new_post(db, data)

@router.patch("/admin/posts/{post_id}", response_model=PostAdmin, dependencies=[Depends(require_admin)])
async def update_post(
    post_id: int,
    data: PostUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление поста

    доступно только ADMIN

    принимает:
        id поста
        title: новый заголовок (опционально)
        content: новый текст (опционально)
        content_html: новый HTML (опционально)
        category_id: новая категория (опционально)
        slug: новый slug (опционально)

    HTML очищается от XSS через bleach

    возвращает:
        id
        title
        slug
        content: str
        content_html
        created_at
        updated_at
        author_id
        category_id
        author (объект класса UserAdmin)
        category (объект класса CategoryAdmin)
    """
    return await update_existing_post(db, post_id, data)

@router.delete("/admin/posts/{post_id}", dependencies=[Depends(require_admin)])
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Удаление поста

    доступно только ADMIN

    принимает id поста

    возвращает confirmation message
    """
    return await delete_existing_post(db, post_id)