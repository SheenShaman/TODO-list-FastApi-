from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from contextlib import asynccontextmanager

engine = create_async_engine(settings.database_url, echo=True)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


@asynccontextmanager
async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase):
    pass
