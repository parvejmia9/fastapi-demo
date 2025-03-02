from .base import Base
from typing import Optional
from sqlalchemy.orm import Mapped ,mapped_column,relationship
from sqlalchemy import  Integer,String,ForeignKey,DateTime,func
    

class Room(Base):
    __tablename__ = "rooms"
    room_id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    room_name: Mapped[String]= mapped_column(String(),nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id",ondelete="SET NULL"), nullable=True)  # Foreign Key

    user=relationship("User",back_populates="rooms")
    messages=relationship("Message",back_populates="room",cascade="all, delete")  
