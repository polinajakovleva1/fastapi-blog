from pydantic import BaseModel, model_validator
from typing import Optional
from slugify import slugify
from datetime import datetime
from .user import UserPublic, UserAdmin
from .category import CategoryPublic, CategoryAdmin

class PostCreate(BaseModel):
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
    title: str
    slug: str
    content: str
    content_html: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: UserPublic
    category: CategoryPublic
    
    class Config:
        from_attributes = True

class PostAdmin(BaseModel):
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
    
    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
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
