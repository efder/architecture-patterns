from datetime import timedelta
from model import *

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("oder-123", sku, line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 10, 8)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 8, 10)
    assert batch.can_allocate(line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 10, 10)
    assert batch.can_allocate(line)


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_deallocate():
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


