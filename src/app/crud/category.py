from sqlalchemy.orm import Session
from ..models.category import Category
from ..schemas.category import CategoryCreate

def create_test_category(db: Session):
    if not db.query(Category).first():
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

    return db.query(Category).all()