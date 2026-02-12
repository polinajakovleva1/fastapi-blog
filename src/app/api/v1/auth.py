from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.security import verify_password, create_access_token, create_refresh_token, decode_token
from ...crud.user import create_user, get_user

async def auth_user(db: AsyncSession, email: str, password: str):
    user = await get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def register_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await get_user(db, form_data.username)
    if user:
        raise HTTPException(status_code=400, detail="email is busy")
    else:
        await create_user(db, form_data.username, form_data.password)
    return await login_user(form_data, db)

async def login_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await auth_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


async def refr_token(refresh_token: str, db: AsyncSession):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid token type")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await get_user(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    new_access_token = create_access_token({"sub": user.email})
    new_refresh_token = create_refresh_token({"sub": user.email})
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
