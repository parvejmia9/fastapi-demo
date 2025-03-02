from pydantic import BaseModel
from src.models.room_model import Room
class RoomCreate(BaseModel):
    room_name: str

class RoomCreationResponse(BaseModel):
    room_id: int
    room_name: str
    user_id: int

    class Config:
        orm_mode = True
   


class RoomList(BaseModel):
    Room