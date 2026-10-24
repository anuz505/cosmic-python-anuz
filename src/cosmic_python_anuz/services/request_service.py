
from cosmic_python_anuz.exceptions.exception import InvalidSku
from cosmic_python_anuz.models.value_objects import Orderline
from cosmic_python_anuz.services.unit_of_work import AbstractUoW
from cosmic_python_anuz.models.entities import Product

async def AllocateService(line: Orderline, uow: AbstractUoW) -> str:
    async with uow:
        product = await uow.products_repo.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid Sku {line.sku}")
        batch_ref = product.allocate(line)
        await uow.commit()
    return batch_ref

async def DeallocateService(line: Orderline, uow: AbstractUoW) -> str:
    async with uow:
        product = await uow.products_repo.get(line.sku)
        if product is None:
            raise InvalidSku(f"Invalid Sku {line.sku}")
        batch_ref = product.deallocate(line=line)
        await uow.commit()
    return batch_ref
