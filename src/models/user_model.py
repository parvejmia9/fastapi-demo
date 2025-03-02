from .base import Base

from sqlalchemy.orm import Mapped ,mapped_column,relationship
from sqlalchemy import  Integer, String

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    full_name: Mapped[str] = mapped_column(String(),nullable=False)
    email:Mapped[str]=mapped_column(String(),nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(String(),nullable=False)
    role: Mapped[str] = mapped_column(String(),nullable=False,default="user")

    
    rooms = relationship("Room", back_populates="user")
    messages = relationship("Message",back_populates="user")
