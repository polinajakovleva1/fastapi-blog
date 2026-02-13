import bcrypt
import jwt
from jwt import PyJWTError
from fastapi import HTTPException
from .config import settings
from datetime import datetime, timedelta, UTC

def get_password_hash(password: str):
    """
    Хэширование пароля с помощью bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed: str):
    """
    Проверка совпадения пароля и хэша с помощью bcrypt
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def create_refresh_token(data: dict):
    """
    Создание refresh токена
    
    срок жизни REFRESH_TOKEN_EXPIRE_DAYS из настроек
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": int(expire.timestamp()),
        "type": "refresh"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(data: dict):
    """
    Создание access токена
    
    срок жизни ACCESS_TOKEN_EXPIRE_DAYS из настроек
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": int(expire.timestamp()),
        "type": "access"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    """
    Декодирование и проверка JWT токена

    если токен недействителен вернет HTTPException 401
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")