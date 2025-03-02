from src.models import async_session
from src.services.user_service import UserService
from fastapi import Cookie, Depends, HTTPException
user_service=UserService()

async def get_db():
    db=async_session()
    try:
        yield db
    except:
        await db.rollback()
        raise
    else:
        await db.commit()
    finally:
        await db.close()

async def get_current_user(
    session_token: str = Cookie(None),  # Get session_token from Cookie
    session=Depends(get_db)  # Inject database session
):
    if not session_token:
        raise HTTPException(status_code=401, detail="Unauthorized: No session token")

    user = await user_service.get_current_user(session_token=session_token, session=session)
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid session token")

    return user