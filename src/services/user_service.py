from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.user_schema import UserList,UserCreationResponse,UserCreate
from src.models import User,SessionToken
from src.utills import hash_password, verify_password


class UserService():
    async def get_users(self,session:AsyncSession):
        stm=select(User)
        print("Executing Query:", stm)
        res= await session.execute(stm)
        if res==None:
            return []
        return res.scalars().all()
    
    async def get_user_by_id(self,user_id:int,session:AsyncSession):
        print("***************",type(user_id))
        stm=select(User).where(User.id == user_id)
        res= await session.execute(stm)
        if res==None:
            return []
        print("*****res: ",res)
        return res.scalars().first()
        
    async def add_user(self,payload:UserCreate,session: AsyncSession):
        user_dict=payload.model_dump()
        user_dict["password_hash"]=hash_password(payload.password)
        del user_dict["password"]
        user=User(**user_dict)
        session.add(user)
        await session.flush()
        print("***user:",user.__dict__)
        return user
    
    async def authenticate_user(self,email:str,password:str,session:AsyncSession):
        stm=select(User).where(User.email==email)
        res= await session.execute(stm)
        if res==None:
            return None
        user=res.scalars().first()
        if user and verify_password(password,user.password_hash):
            return user
        return None
    
    async def get_current_user(self,session_token:str,session:AsyncSession):
        stm=select(SessionToken).where(SessionToken.session_token==session_token)
        res= await session.execute(stm)
        if res==None:
            return None
        st=res.scalars().first()
        if st:
            return await self.get_user_by_id(st.user_id,session)
        return None