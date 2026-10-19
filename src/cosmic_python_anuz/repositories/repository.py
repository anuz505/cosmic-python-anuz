import abc

from cosmic_python_anuz.models import entities


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, batch: entities.Batch):
        pass

    @abc.abstractmethod
    async def get(self, ref) -> entities.Batch:
        pass
