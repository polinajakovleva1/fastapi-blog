from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime
from slugify import slugify

class CategoryCreate(BaseModel):
    """
    Схема для создания новой категории

    Принимает:
        name: название категории (обязательно)
        slug: URL-идентификатор (опционально, генерируется из name)
    """
    name: str
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'name' in data:
            data['slug'] = slugify(data['name'])
        return data
    
class CategoryPublic(BaseModel):
    """Публичные данные категории"""
    name: str
    slug: str
    
    model_config = {
        "from_attributes": True
    }

class CategoryAdmin(BaseModel):
    """Закрытые данные категории для отображения в объектах класса PostAdmin"""
    id: int
    name: str
    slug: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class CategoryUpdate(BaseModel):
    """
    Схема для обновления категории

    принимает:
        name: новое название (опционально)
        slug: новый URL-идентификатор (опционально, генерируется из name)
    """
    name: Optional[str] = None
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'name' in data and not data.get('slug'):
            data['slug'] = slugify(data['name'])
        return data