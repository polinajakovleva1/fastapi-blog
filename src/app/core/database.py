from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase,  sessionmaker
from .config import settings

database_url = settings.DATABASE_URL

engine = create_async_engine(
    database_url, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase): pass

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
