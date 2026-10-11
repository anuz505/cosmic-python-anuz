from datetime import date

from cosmic_python_anuz.models.value_objects import Orderline


class Batch:
    def __init__(self, ref_id: str, sku: str, quantity: int, eta: date | None = None):
        self.ref = ref_id
        self.sku = sku
        self._purchased_quantity = quantity
        self.eta = eta
        self.allocations = set()

    def allocate(self, orderline: Orderline):
        if self.can_allocate(orderline):
            self.allocations.add(orderline)

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return self.ref == other.ref # since two batches are considered equal if their references are equal

    def __hash__(self):
        return hash(self.ref) # since python set requires their elements to be hashable.

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self.allocations)

    def can_allocate(self, line: Orderline):
        return self.sku == line.sku and line.quantity <=self.available_quantity
