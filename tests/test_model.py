from datetime import date

from cosmic_python_anuz.models.entities import Batch
from cosmic_python_anuz.models.value_objects import Orderline


def make_batch_and_line_for_test(sku, batch_qty, line_qty):
    return(
        Batch(ref_id="batch_001", sku=sku, quantity=batch_qty, eta=date.today()),
        Orderline(reference_id="order-001", sku=sku, quantity=line_qty)
    )
def test_cannot_allocate_if_available_is_less_than_ordered():
    small_batch, large_orderline = make_batch_and_line_for_test(sku="BLUE-TABLE-01", batch_qty=10, line_qty=20)
    assert small_batch.can_allocate(large_orderline) is False

def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-002", "なにか", 2, eta=None)
    different_sku_line = Orderline("order-002", sku="日本　チャイル", quantity=2 )
    assert not batch.can_allocate(different_sku_line)

def test_allocations_are_idempotent():
    batch, line = make_batch_and_line_for_test("RED-TABLE", 20, 10)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 10

def test_deallocate():
    batch, line = make_batch_and_line_for_test("RED-CHAIR", 20, 10)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20

def test_can_allocate_if_equal_or_more():
    batch, line = make_batch_and_line_for_test("BLACK-MOUSE", 50, 10)
    batch.allocate(line)
    new_batch, new_line = make_batch_and_line_for_test("WHITE-MOUSE", 20, 20)
    new_batch.allocate(new_line)
    assert new_batch.available_quantity == 0
    assert batch.available_quantity == 40
