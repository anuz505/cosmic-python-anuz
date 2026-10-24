from cosmic_python_anuz.adapters.sql_repository import PostgreSQLRepository
from cosmic_python_anuz.config.settings import DEFAULT_SESSION_FACTORY
from cosmic_python_anuz.services.unit_of_work import AbstractUoW


class PostgreSQLUoW(AbstractUoW):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> AbstractUoW:
        self.session = self.session_factory()
        self.products_repo = PostgreSQLRepository(self.session) # batches_repo cause this is a repo instance but in the book batches is written so that the maybe read like a business logic rather than just database.
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
