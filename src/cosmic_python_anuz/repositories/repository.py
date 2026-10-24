import abc

from cosmic_python_anuz.models import entities


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, product: entities.Product):
        pass

    @abc.abstractmethod
    async def get(self, sku: str) -> entities.Product:
        pass
