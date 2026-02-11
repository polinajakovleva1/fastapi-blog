from fastapi import FastAPI, Depends
from .core.config import settings
from .core.database import engine, Base, get_db
from .crud.user import create_test_users
from .crud.category import create_test_category
from .crud.post import create_test_post
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="FastAPI Blog Backend",
    description="Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователями",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    return await create_test_post(db, 0, 1)
