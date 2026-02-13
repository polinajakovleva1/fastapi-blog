from ..core.database import Base
from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    posts = relationship("Post", back_populates="category", cascade="all, delete-orphan")