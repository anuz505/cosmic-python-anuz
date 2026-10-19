from cosmic_python_anuz.models.entities import Batch
from cosmic_python_anuz.repositories.repository import AbstractRepository


class PostgreSQLRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, batch):
        await self.session.add(batch)

    async def get(self, ref):
            return await self.session.query(Batch).filter_by(ref=ref).one()

    async def list(self):
            return await self.session.query(Batch).all()
