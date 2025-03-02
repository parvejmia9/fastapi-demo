from .base import Base
from sqlalchemy.orm import Mapped ,mapped_column
from sqlalchemy import  Integer,String

class SessionToken(Base):
    __tablename__ = "session_tokens"
    session_token_id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    session_token: Mapped[String]= mapped_column(String(),nullable=False,unique=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Foreign Key
    
    
    