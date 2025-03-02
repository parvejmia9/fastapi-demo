from fastapi import APIRouter, Depends, HTTPException, status, Response, Request,Cookie
from src.schemas.user_schema import UserList, UserCreationResponse, UserCreate, UserLogin
from typing import List, Optional
from src.dependencies import get_db
from sqlalchemy import select
from src.models import User
from src.services.user_service import UserService
from src.services.sessionToken_service import SessionTokenService
from src.utills import create_session_token

user_service = UserService()
session_service = SessionTokenService()

router = APIRouter()


@router.get("/users", response_model=List[UserCreationResponse])
async def list_users(session=Depends(get_db)):
    users = await user_service.get_users(session=session)
    print("*************** ", users)
    return users


@router.post("/users/login",response_model=None)
async def login_user(
    payload: UserLogin,response: Response, session=Depends(get_db)
):
    user = await user_service.authenticate_user(
        email=payload.email, password=payload.password, session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    else:
        session_token = create_session_token()
        try:
            if response:
                response.set_cookie(
                    key="cur_user", value=session_token, httponly=True
                )

            await session_service.add_session_token(
                user_id=user.id, session_token=session_token, session=session
            )
            return {"cur_user": session_token}
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )


@router.post("/users/logout",response_model=None)
async def logout_user(
    response: Response,
    request: Request,
    session=Depends(get_db),
    
):
    try:
        session_token = request.cookies.get("cur_user")
        if session_token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session token is missing",
            )
        await session_service.delete_session_token(
            session_token=session_token, session=session
        )
        if response:
            response.delete_cookie(key="session_token")
        return {"message": "Logged Out Successfully"}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/users/me", response_model=UserCreationResponse)
async def get_current_user(
    request: Request,
    session=Depends(get_db),
    
):
    session_token = request.cookies.get("cur_user")
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session token is missing",
        )
    user = await user_service.get_current_user(
        session_token=session_token, session=session
    )
    return user


@router.get("/users/{user_id}", response_model=UserCreationResponse)
async def view_user(user_id: int, session=Depends(get_db)):
    user = await user_service.get_user_by_id(user_id=user_id, session=session)
    return user


@router.post("/user", response_model=UserCreationResponse)
async def create_user(payload: UserCreate, session=Depends(get_db)):
    print("****payload: ", payload)
    user = await user_service.add_user(payload=payload, session=session)
    print("*************** ", user.__dict__)
    return user
