from fastapi import Depends
from ...core.dependencies import get_current_user
from ...models.user import User

async def get_me(current_user: User = Depends(get_current_user)):
    return current_user