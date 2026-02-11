from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from .config import settings

database_url = settings.DATABASE_URL

engine = create_engine(
    database_url, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase): pass

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
