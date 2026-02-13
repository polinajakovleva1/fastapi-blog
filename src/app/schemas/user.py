from pydantic import BaseModel

class UserPublic(BaseModel):
    """Публичные данные пользователя"""
    email: str
    role: str
    
    model_config = {
        "from_attributes": True
    }

class UserAdmin(BaseModel):
    """Закрытые данные пользователя для отображения в объектах класса PostAdmin"""
    id: int
    email: str
    role: str
    
    model_config = {
        "from_attributes": True
    }