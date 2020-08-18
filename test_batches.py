from datetime import date, timedelta
from model import *
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


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
    assert batch.can_allocate(line) == True

def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 8, 10)
    assert batch.can_allocate(line) == False

def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 10, 10)
    assert batch.can_allocate(line) == True

def  test_can_allocate_if_skus_are_same():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 10)
    assert batch.can_allocate(line) == True

def test_cannot_allocate_if_skus_are_different():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "DESK-LAMP", 10)
    assert batch.can_allocate(line) == False

def test_cannot_allocate_same_line_twice():
    batch = Batch("batch-001", "SMALL-TABLE", qty=30, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 10)
    assert batch.can_allocate(line) == True
    batch.allocate(line)
    assert batch.can_allocate(line) == False

def test_prefers_warehouse_batches_to_shipments():
    batch_in_warehouse, line = make_batch_and_line("DESK-LAMP", 10, 8)
    batch_tomorrow = Batch("batch-002", "DESK-LAMP", 10, tomorrow)
    batches = Batches()
    batches.add_batch(batch_in_warehouse)
    batches.add_batch(batch_tomorrow)
    selected_batch = batches.allocate_to(line)
    assert selected_batch == batch_in_warehouse
    
def test_prefers_earlier_batches():
    batch_in_warehouse, line = make_batch_and_line("DESK-LAMP", 10, 8)
    batch_tomorrow = Batch("batch-002", "DESK-LAMP", 10, tomorrow)
    batch_later = Batch("batch-003", "DESK-LAMP", 10, later)
    batches = Batches()
    batches.add_batch(batch_in_warehouse)
    batches.add_batch(batch_tomorrow)
    batches.add_batch(batch_later)
    selected_batch = batches.allocate_to(line)
    assert selected_batch == batch_in_warehouse