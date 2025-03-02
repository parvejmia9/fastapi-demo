from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,desc,and_
from src.schemas.message_schema import MessageCreate
from src.models import Message

class MessageService():
    async def get_messages_of_a_room(self,room_id:int,session:AsyncSession):
        stm=select(Message).where(Message.room_id==room_id).order_by(desc(Message.created_at))
        res= await session.execute(stm)
        if res==None:
            return []
        return res.scalars().all()
    
    async def get_message_by_id(self,room_id:int,message_id:int,session:AsyncSession):
        stm=select(Message).where(and_(Message.room_id == room_id, Message.message_id == message_id))
        res= await session.execute(stm)
        if res==None:
            return []
        return res.scalars().first()
    
    async def add_message(self,room_id:int,user_id:int,payload:MessageCreate,session: AsyncSession):
        message_dict=payload.model_dump()
        message_dict["room_id"]=room_id
        message_dict["user_id"]=user_id
        print("----------",message_dict)
        message=Message(**message_dict)
        session.add(message)
        await session.flush()
        print("***room:",Message.__dict__)
        return message