from sqlalchemy.orm import Session
from ..models.post import Post
from ..schemas.post import PostCreate

def create_test_post(db: Session, author_id: int, category_id: int):
    if not db.query(Post).first():
        posts_data = [
            PostCreate(
                title="Первый пост",
                content="Содержание первого поста",
                author_id=author_id,
                category_id=category_id
            )
        ]

        posts = []
        
        for data in posts_data:
            post = Post(
                title=data.title,
                slug=data.slug,
                content=data.content,
                author_id=data.author_id,
                category_id=data.category_id
            )
            posts.append(post)

        db.add_all(posts)
        db.commit()

    return db.query(Post).all()