from ..core.database import Base
from sqlalchemy import  Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    content_html = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="posts", lazy="selectin")
    category = relationship("Category", back_populates="posts", lazy="selectin")