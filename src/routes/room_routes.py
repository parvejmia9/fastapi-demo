from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.schemas.room_schema import RoomCreationResponse, RoomCreate
from typing import List
from src.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.models.room_model import Room
from src.services.room_service import RoomService
from src.services.user_service import UserService
from typing_extensions import Annotated

room_service = RoomService()
user_service = UserService()

router = APIRouter()


@router.get("/rooms", response_model=List[RoomCreationResponse])
async def list_rooms(session=Depends(get_db)):
    rooms = await room_service.get_rooms(session=session)
    return rooms


@router.post("/room")
async def create_room(
    request: Request,
    payload: RoomCreate,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    session_token = request.cookies.get("cur_user")
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token is missing",
            headers={"WWW-Authenticate": "Basic"},
        )
    current_user = await user_service.get_current_user(
        session_token=session_token, session=session
    )
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    room = await room_service.add_room(
        payload=payload, user_id=current_user.id, session=session
    )

    return room
