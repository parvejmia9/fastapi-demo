from __future__ import annotations

import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload

db_url = "sqlite+aiosqlite:///test.db"

engine=create_async_engine(db_url,echo=True)
async_session=async_sessionmaker(engine,expire_on_commit=False)
class Base(AsyncAttrs, DeclarativeBase):
   pass