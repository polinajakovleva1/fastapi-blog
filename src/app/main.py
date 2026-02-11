from fastapi import FastAPI
from .core.config import settings

app = FastAPI(
    title="FastAPI Blog Backend",
    description="Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователями",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "project_name": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL,
        "jwt_algorithm": settings.ALGORITHM,
        "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_token_expire_days": settings.REFRESH_TOKEN_EXPIRE_DAYS,
        "secret_key_set": settings.SECRET_KEY
    }