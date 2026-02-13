from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime
from slugify import slugify

class CategoryCreate(BaseModel):
    name: str
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'name' in data:
            data['slug'] = slugify(data['name'])
        return data
    
class CategoryPublic(BaseModel):
    name: str
    slug: str
    
    class Config:
        from_attributes = True

class CategoryAdmin(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'name' in data and not data.get('slug'):
            data['slug'] = slugify(data['name'])
        return data