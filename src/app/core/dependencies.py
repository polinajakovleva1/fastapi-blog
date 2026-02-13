from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from .config import settings
from .database import get_db
from ..crud.user import get_user, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Получение текущего пользователя из JWT токена:
        извлекает токен из заголовка Authorization
        декодирует JWT, проверяет подпись и срок действия
        загружает пользователя из БД по email (sub)

    если токен недействителен или пользователь не найден вернет HTTPException 401 
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_admin(user: User = Depends(get_current_user)) -> None:
    """
    Проверка прав администратора

    используется как зависимость в админ-эндпоинтах
    
    если пользователь не ADMIN вернет HTTPException 403
    """
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin privileges required")