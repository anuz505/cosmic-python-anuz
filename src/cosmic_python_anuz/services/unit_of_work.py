import abc

from cosmic_python_anuz.repositories.repository import AbstractRepository


class AbstractUoW(abc.ABC):
    batches_repo: AbstractRepository

    async def __aenter__(self) -> AbstractUoW:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abc.abstractmethod
    async def rollback(self):
        pass

    @abc.abstractmethod
    async def commit(self):
        pass
