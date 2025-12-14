from typing import TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.orm import DeclarativeBase

from app.db.postgres.session import get_session

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepo:
    model: type[T]

    @classmethod
    async def create(cls, **kwargs) -> T:
        async with get_session() as session:
            obj = cls.model(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def get_all(cls) -> list[T]:
        async with get_session() as session:
            result = await session.execute(select(cls.model))
            return result.scalars().all()

    @classmethod
    async def get_all_by_kwargs(cls, **kwargs: dict) -> T | None:
        async with get_session() as session:
            result = await session.execute(
                select(cls.model).filter_by(**kwargs)
            )
            return result.scalars().all()

    @classmethod
    async def get_one_by_id(cls, id_: int) -> T | None:
        async with get_session() as session:
            result = await session.execute(
                select(cls.model).where(cls.model.id == id_)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_kwargs(cls, **kwargs: dict) -> T | None:
        async with get_session() as session:
            result = await session.execute(
                select(cls.model).filter_by(**kwargs)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def update_by_id(cls, id_: int, **kwargs) -> T:
        async with get_session() as session:
            await session.execute(
                update(cls.model).where(cls.model.id == id_).values(**kwargs)
            )
            await session.commit()

            result = await session.execute(
                select(cls.model).where(cls.model.id == id_)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, id_: int) -> None:
        async with get_session() as session:
            await session.execute(delete(cls.model).where(cls.model.id == id_))
            await session.commit()
