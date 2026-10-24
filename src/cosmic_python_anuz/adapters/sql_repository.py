<<<<<<< Updated upstream
from cosmic_python_anuz.models.entities import Batch
=======
from sqlalchemy import select

from cosmic_python_anuz.models.entities import Product
>>>>>>> Stashed changes
from cosmic_python_anuz.repositories.repository import AbstractRepository


class PostgreSQLRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

<<<<<<< Updated upstream
    async def add(self, batch):
        await self.session.add(batch)

    async def get(self, ref):
            return await self.session.query(Batch).filter_by(ref=ref).one()

    async def list(self):
            return await self.session.query(Batch).all()
=======
    async def add(self, product):
        self.session.add(product)

    async def get(self, sku: str):
        # smt = select(Batch).options(selectinload(Batch.allocations)).filter_by(ref=ref)
        smt = select(Product).filter_by(sku=sku)
        result = await self.session.execute(smt)
        return result.scalar_one()
#
#     async def list(self):
#         smt = select(Batch).options(selectinload(Batch.allocations))
#         result = await self.session.execute(smt)
#         return list(result.scalars().all())
>>>>>>> Stashed changes
