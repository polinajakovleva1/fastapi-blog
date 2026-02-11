from fastapi import FastAPI
from .core.config import settings
from .core.database import engine, Base, get_db
from .crud.user import create_test_users
from sqlalchemy.orm import Session
from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Blog Backend",
    description="Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователями",
    version="1.0.0"
)

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return create_test_users(db)
