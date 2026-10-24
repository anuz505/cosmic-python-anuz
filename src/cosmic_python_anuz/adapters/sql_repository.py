from sqlalchemy import select

from cosmic_python_anuz.models.entities import Product
from cosmic_python_anuz.repositories.repository import AbstractRepository


class PostgreSQLRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, product):
        self.session.add(product)

    async def get(self, sku: str):
        smt = select(Product).filter_by(sku=sku)
        result = await self.session.execute(smt)
        return result.scalar_one()
