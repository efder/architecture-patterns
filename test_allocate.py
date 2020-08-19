from model import Batch, OrderLine, allocate, OutOfStock
from datetime import date, timedelta
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_warehouse_batches_to_shipments():
    batch_in_warehouse = Batch("batch-001", "DESK-LAMP", 100, None)
    batch_tomorrow = Batch("batch-002", "DESK-LAMP", 100, tomorrow)
    line = OrderLine("oref", "DESK-LAMP", 10)
    batches = [batch_in_warehouse, batch_tomorrow]
    selected_batch_ref = allocate(line, batches)
    assert selected_batch_ref == batch_in_warehouse.reference and batch_in_warehouse.available_quantity == 90


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    selected_batch_ref = allocate(line, [medium, earliest, latest])
    assert selected_batch_ref == earliest.reference and earliest.available_quantity == 90

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])


