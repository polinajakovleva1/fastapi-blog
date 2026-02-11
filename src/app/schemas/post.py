from pydantic import BaseModel, model_validator
from typing import Optional
from slugify import slugify

class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int
    author_id: int
    slug: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, data):
        if isinstance(data, dict) and 'title' in data:
            data['slug'] = slugify(data['title'])
        return data