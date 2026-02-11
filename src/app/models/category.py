from ..core.database import Base
from sqlalchemy import  Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func

class Category(Base):
    __tablename__ = "categories"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)