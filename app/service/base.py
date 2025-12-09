from typing import Type

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    model = Type

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int):
        result = await session.execute(select(cls.model).filter_by(id=model_id))
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filters):
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filters):
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **date):
        query = insert(cls.model).values(**date)
        await session.execute(query)
        await session.commit()
