from pydantic import BaseModel, model_validator
from typing import Optional
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