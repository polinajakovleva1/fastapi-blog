"""
Скрипт для создания администратора по умолчанию
Запуск: python -m src.scripts.create_admin
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.app.core.config import settings
from src.app.crud.user import create_user, get_user
from src.app.models.user import User

DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_PASSWORD = "admin123"

async def create_admin():
    database_url = settings.DATABASE_URL

    engine = create_async_engine(
        database_url, connect_args={"check_same_thread": False}
    )

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        exist_admin = await db.execute(select(User).where(User.role == "ADMIN"))
        admin = exist_admin.scalar_one_or_none()
        if admin:
            print("Пользователь с ролью ADMIN уже есть в системе")
            print(f"email: {admin.email}")
            return
        exist_user = await get_user(db, DEFAULT_ADMIN_EMAIL)
        if exist_user:
            exist_user.role = "ADMIN"
            await db.commit()
            await db.refresh(exist_user)
            print("Пользователь с ролью ADMIN создан")
            return
        admin = await create_user(db, email=DEFAULT_ADMIN_EMAIL, password=DEFAULT_ADMIN_PASSWORD)
        admin.role = "ADMIN"
        await db.commit()
        await db.refresh(admin)
        print("Пользователь с ролью ADMIN создан")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_admin())