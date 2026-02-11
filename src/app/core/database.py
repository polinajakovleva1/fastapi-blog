from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import sessionmaker
from .config import settings

database_url = settings.DATABASE_URL

engine = create_engine(
    database_url, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase): pass
class Test(Base):
    __tablename__ = "test"
 
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
