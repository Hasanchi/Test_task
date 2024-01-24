from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker


class AbstractRepository(ABC):

    @abstractmethod
    async def select_all():
        raise NotImplementedError

    @abstractmethod
    async def select_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def select_all(self):
        async with async_session_maker() as session:
            query = select(self.model)
            results = await session.execute(query)
            results = [row[0].to_read_model() for row in results.all()]
            return results

    async def add_one(self, **dict):
        async with async_session_maker() as session:
            query = insert(self.model).values(**dict).returning(self.model.id)
            results = await session.execute(query)
            await session.commit()
            return results.scalar_one()
