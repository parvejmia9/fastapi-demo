from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.schemas.message_schema import MessageCreationResponse,MessageCreate
from typing import List
from src.dependencies import get_db
from sqlalchemy import select
from src.models import User
from src.services.message_service import MessageService
from src.services.user_service import UserService
message_service=MessageService()
user_service=UserService()
 

router = APIRouter()


@router.get("/rooms/{room_id}/messages", response_model=List[MessageCreationResponse])
async def list_messages(room_id:int,session= Depends(get_db)):
    messages=await message_service.get_messages_of_a_room(room_id=room_id,session=session)
    return messages

@router.get("/rooms/{room_id}/messages/{message_id}",response_model=MessageCreationResponse)
async def view_a_message(room_id: int,message_id:int,session=Depends(get_db)):
    message=await message_service.get_message_by_id(room_id=room_id,message_id=message_id,session=session)
    return message

@router.post("/rooms/{room_id}/messages",response_model=MessageCreationResponse)
async def create_message(request:Request,room_id:int,payload:MessageCreate,session= Depends(get_db)):
    print("****payload: ",payload)
    session_token = request.cookies.get("cur_user")
    print("****session_token: ",session_token)
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token is missing",
        )
    current_user = await user_service.get_current_user(
        session_token=session_token, session=session
    )
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    user=await message_service.add_message(user_id=current_user.id,room_id=room_id,payload=payload,session=session)
    print("*************** ",user.__dict__)
    return user



