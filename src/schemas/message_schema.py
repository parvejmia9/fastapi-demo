from pydantic import BaseModel
from src.models.message_model import Message
from typing import Optional
from sqlalchemy.orm import Mapped
class MessageCreate(BaseModel):
    message_content: str

class MessageCreationResponse(BaseModel):
    message_content: str
    room_id: int
    user_id: int

    class Config:
        orm_mode = True

