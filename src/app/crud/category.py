from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate

async def get_categories(db: AsyncSession):
    """Получение списка всех объектов класса Category"""
    result = await db.execute(select(Category))
    return result.scalars().all()

async def get_categories_slug(db: AsyncSession, slug: str):
    """Получение объекта класса Category с указанным slug"""
    result = await db.execute(select(Category).where(Category.slug==slug))
    return result.scalar_one_or_none()

async def get_category_by_id(db: AsyncSession, category_id: int):
    """Получение объекта класса Category с указанным id"""
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category

async def generate_unique_slug(db: AsyncSession, base_slug: str, exclude_id: int = None):
    """
    Генерация уникального slug
    если slug занят, добавляет к нему значение counter
    """
    slug = base_slug
    counter = 1
    while True:
        existing = await get_categories_slug(db, slug)
        if not existing or (exclude_id and existing.id == exclude_id):
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1

async def create_category(db: AsyncSession, data: CategoryCreate):
    """Создание объекта класса Category"""
    unique_slug = await generate_unique_slug(db, data.slug)
    data.slug = unique_slug
    category = Category(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

async def update_category(db: AsyncSession, category_id: int, data: CategoryUpdate):
    """Обновление объекта класса Category"""
    category = await get_category_by_id(db, category_id)
    if data.name is not None:
        category.name = data.name
    if data.slug is not None:
        unique_slug = await generate_unique_slug(db, data.slug, exclude_id=category_id)
        category.slug = unique_slug
    await db.commit()
    await db.refresh(category)
    return category

async def delete_category(db: AsyncSession, category_id: int):
    """Удаление объекта класса Category"""
    category = await get_category_by_id(db, category_id)
    await db.delete(category)
    await db.commit()
    return {"message": "Category deleted successfully"}
