from pydantic import BaseModel, model_validator
from typing import Optional
from slugify import slugify
from datetime import datetime
from .user import UserPublic, UserAdmin
from .category import CategoryPublic, CategoryAdmin

class PostCreate(BaseModel):
    """
    Схема для создания поста

    принимает:
        title: название поста (обязательно)
        content: содержание поста (обязательно)
        content_html: html содержания поста (опционально)
        category_id: id категории (обязательно)
        author_id: id автора (обязательно)
        slug: URL-идентификатор (опционально, генерируется из name)
    """
    title: str
    content: str
    content_html: Optional[str] = None
    category_id: int
    author_id: int
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'title' in data:
            data['slug'] = slugify(data['title'])
        return data
    
class PostPublic(BaseModel):
    """Публичные данные поста"""
    title: str
    slug: str
    content: str
    content_html: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: UserPublic
    category: CategoryPublic
    
    model_config = {
        "from_attributes": True
    }

class PostAdmin(BaseModel):
    """Закрытые данные поста"""
    id: int
    title: str
    slug: str
    content: str
    content_html: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author_id: int
    category_id: int
    author: UserAdmin
    category: CategoryAdmin
    
    model_config = {
        "from_attributes": True
    }

class PostUpdate(BaseModel):
    """
    Схема для обновления категории

    принимает:
        title: новое название поста (опционально)
        content: новое содержание поста (опционально)
        content_html: новый html содержания поста (опционально)
        category_id: новый id категории (опционально)
        slug: новый URL-идентификатор (опционально, генерируется из title)
    """
    title: Optional[str] = None
    content: Optional[str] = None
    content_html: Optional[str] = None
    category_id: Optional[int] = None
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'title' in data and not data.get('slug'):
            data['slug'] = slugify(data['title'])
        return data
