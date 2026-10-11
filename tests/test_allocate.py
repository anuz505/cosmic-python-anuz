import pytest
from datetime import date, timedelta
from cosmic_python_anuz.models.entities import Batch, Orderline, allocate
from cosmic_python_anuz.exceptions.exception import OutOfStock, InvalidSku
today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_raises_out_of_stock_exception():
    batch = Batch("batch-001", "small-bag", 10, eta=None)
    allocate(Orderline("order-001", "small-bag", 10), [batch])
    with pytest.raises(OutOfStock, match="small-bag"):
        allocate(Orderline("order-002", "small-bag", 1), [batch])


def test_prefer_current_stock_rather_than_shipment():
    in_stock_batch = Batch("batch-001", "STEEL-BOTTLE", 20, eta=None)
    shipment_batch = Batch("batch-002", "STEEL-BOTTLE", 20, eta=tomorrow)
    line = Orderline("order-01", "STEEL-BOTTLE",10)
    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 10
    assert shipment_batch.available_quantity == 20

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = Orderline("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100
