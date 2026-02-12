from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserPublic(BaseModel):
    email: str
    role: str
    
    class Config:
        from_attributes = True