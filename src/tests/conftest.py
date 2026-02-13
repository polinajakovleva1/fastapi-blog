import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.app.core.database import Base, get_db
from src.app.main import app
from src.app.crud.user import create_user
from src.app.core.security import create_access_token
from src.app.core.security import create_refresh_token
from src.app.crud.category import create_category
from src.app.schemas.category import CategoryCreate
from src.app.crud.post import create_post
from src.app.schemas.post import PostCreate

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(engine):
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session):
    user = await create_user(db_session, email="user@test.com", password="user123")
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def admin_user(db_session):
    user = await create_user(db_session, email="admin@test.com", password="admin123")
    user.role = "ADMIN"
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def user_token_access(test_user):
    return create_access_token({"sub": test_user.email})

@pytest.fixture
async def user_token_refresh(test_user):
    return create_refresh_token({"sub": test_user.email})

@pytest.fixture
async def admin_token(admin_user):
    return create_access_token({"sub": admin_user.email})

@pytest.fixture
async def auth_headers(user_token_access):
    return {"Authorization": f"Bearer {user_token_access}"}

@pytest.fixture
async def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
async def test_category(db_session):
    category = await create_category(db_session, CategoryCreate(name="Тестовая категория"))
    await db_session.commit()
    return category

@pytest.fixture
async def test_post(db_session, test_category, test_user):
    post = await create_post(
        db_session,
        PostCreate(
            title="Тестовый пост",
            content="Содержание",
            content_html="<p>Содержание</p>",
            category_id=test_category.id,
            author_id=test_user.id
        )
    )
    await db_session.commit()
    return post