from sqlalchemy.orm import Session
from ..models.user import User

def create_test_users(db: Session):
    if not db.query(User).first():
        user_1 = User(email="email1@mail.com", hashed_password="1234")
        user_2 = User(email="email2@mail.com", hashed_password="5678")
        db.add_all([user_1, user_2])
        db.commit()

    return db.query(User).all()