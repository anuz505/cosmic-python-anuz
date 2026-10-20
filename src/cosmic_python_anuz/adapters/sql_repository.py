from sqlalchemy import select
from sqlalchemy.orm import selectinload

from cosmic_python_anuz.models.entities import Batch
from cosmic_python_anuz.repositories.repository import AbstractRepository


class PostgreSQLRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, batch):
        self.session.add(batch)

    async def get(self, ref):
        smt = select(Batch).options(selectinload(Batch.allocations)).filter_by(ref=ref)
        result = await self.session.execute(smt)
        return result.scalar_one()

    async def list(self):
        smt = select(Batch).options(selectinload(Batch.allocations))
        result = await self.session.execute(smt)
        return list(result.scalars().all())
