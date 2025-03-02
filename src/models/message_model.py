from .base import Base
from typing import Optional
from sqlalchemy.orm import Mapped ,mapped_column,relationship
from sqlalchemy import  String, Integer, ForeignKey, DateTime, func

class Message(Base):
    __tablename__ = "messages"
    message_id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    message_content: Mapped[String]= mapped_column(String(),nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("rooms.room_id"), nullable=False)  # Foreign Key
    room=relationship("Room",back_populates="messages")

    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id",ondelete="SET NULL"), nullable=True)  # Foreign Key
    user=relationship("User",back_populates="messages")
