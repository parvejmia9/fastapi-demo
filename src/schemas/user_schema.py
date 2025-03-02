from pydantic import BaseModel
from src.models.user_model import User
from typing import List
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreationResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: List[UserCreationResponse]
    
    