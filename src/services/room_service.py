from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.room_schema import RoomCreate
from src.models import Room
from src.schemas.room_schema import RoomCreationResponse

class RoomService():
    async def get_rooms(self,session:AsyncSession):
        stm=select(Room)
        res= await session.execute(stm)
        if res==None:
            return []
        print("*****res: ",res)
        return res.scalars().all()
    
    async def add_room(self,payload:RoomCreate,user_id:int,session: AsyncSession)->Room:
        room_dict=payload.model_dump()
        room_dict["user_id"]=user_id
        room=Room(**room_dict)
        session.add(room)
        await session.flush()
        await session.commit() 
        await session.refresh(room)
        print("***room:",room.__dict__)
        return room