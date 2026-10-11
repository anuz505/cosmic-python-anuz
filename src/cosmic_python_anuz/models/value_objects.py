
from dataclasses import dataclass


@dataclass
class Orderline:
    reference_id: str
    sku: str
    quantity: int


@dataclass
class Order:
    orderlines: list[Orderline]
