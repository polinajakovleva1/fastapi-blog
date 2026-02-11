from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.category import Category
from ..schemas.category import CategoryCreate

async def create_test_category(db: AsyncSession):
    result = await db.execute(select(Category))
    if not result.scalars().first():
        categories_data = [
            CategoryCreate(name="Новости"),
            CategoryCreate(name="Технологии")
        ]

        categories = []

        for data in categories_data:
            category = Category(
                name=data.name,
                slug=data.slug
            )
            categories.append(category)

        db.add_all(categories)
        db.commit()

    result = await db.execute(select(Category))
    return result.scalars().all()