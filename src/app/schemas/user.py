from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserPublic(BaseModel):
    email: str
    role: str
    
    model_config = {
        "from_attributes": True
    }

class UserAdmin(BaseModel):
    id: int
    email: str
    role: str
    
    model_config = {
        "from_attributes": True
    }