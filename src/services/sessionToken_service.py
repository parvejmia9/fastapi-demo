from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from src.models import SessionToken
class SessionTokenService:
    async def add_session_token(self, session: AsyncSession, session_token: str, user_id: int):
        stm = insert(SessionToken).values(session_token=session_token, user_id=user_id)
        try:
            await session.execute(stm)
            await session.commit()
        except Exception as e   :
            print("Error: ",e)
            await session.rollback()
            
    async def get_session_token(self, session: AsyncSession, token: str):
        stm = select(SessionToken).where(SessionToken.session_token == token)
        res = await session.execute(stm)
        if res == None:
            return None
        return res.scalars().first()
    
    async def delete_session_token(self, session: AsyncSession, session_token: str):
        stm = select(SessionToken).where(SessionToken.session_token == session_token)
        res = await session.execute(stm)
        if res == None:
            return 
        st = res.scalars().first()
        if st:
            await session.delete(st)
            await session.commit()
        