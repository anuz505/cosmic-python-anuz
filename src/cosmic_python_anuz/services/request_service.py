
from cosmic_python_anuz.adapters.sql_uow import PostgreSQLUoW
from cosmic_python_anuz.models.entities import allocate
from cosmic_python_anuz.models.value_objects import Orderline


async def AllocateService(line: Orderline) -> str:
    async with PostgreSQLUoW() as uow:
        batches = await uow.batches_repo.list()
        batch_ref = allocate(line=line, batches=batches)
        await uow.commit()
    return batch_ref
