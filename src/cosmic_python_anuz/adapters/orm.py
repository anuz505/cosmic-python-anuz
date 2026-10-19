import uuid

from sqlalchemy import Column, Date, MetaData, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from cosmic_python_anuz.models.entities import Batch
from cosmic_python_anuz.models.value_objects import Orderline

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

orderlines = Table(
    "orderlines",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4 ),
    Column("reference_id", UUID, nullable=False),
    Column("sku", String(255), nullable=False),
    Column("quantity", Integer, nullable=False)
)

batches = Table(
    "batches",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("ref", UUID, nullable=False),
    Column("_purchased_qty", Integer, nullable=False, default=1),
    Column("eta", Date, nullable=True)
)
allocations = Table(
    "allocations",
    metadata,
    Column("orderline_id", ForeignKey("orderlines.id"), primary_key=True,ullable=False),
    Column("batch_id",ForeignKey("batches.id"),primary_key=True,nullable=False)
)

def start_mapper():
    mapper_registry.map_imperatively(Orderline, orderlines)
    mapper_registry.map_imperatively(Batch, batches)

    # properties={
    #     "purchased_quantity": batches.c._purchased_qty, if i had the variable purchased_quantity instead of _purchased_quantity
    # },
