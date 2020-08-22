def test_order_lines(session):
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES '
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )

    expected = [(1, 'RED-CHAIR', 12, 'order1'), (2, 'RED-TABLE', 13, 'order1'), (3, 'BLUE-LIPSTICK', 14, 'order2')]
    result = list(session.execute('SELECT * FROM order_lines'))

    assert expected == result

def test_batch(session):
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES ("batch-001", "GENERIC-SOFA", 100, \'2020-08-22\' )'
    )

    result = list(session.execute('SELECT * FROM batches'))
    assert result == [(1, 'batch-001', 'GENERIC-SOFA', 100, '2020-08-22')]

def test_allocation(session):
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES '
        '("test_allocation_order", "RED-CHAIR", 12)'
    )

    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES ("test_allocation_batch", "GENERIC-SOFA", 100, \'2020-08-22\' )'
    )

    session.execute(
        'INSERT INTO allocations (orderline_id, batch_id) '
        'VALUES (1, 1)'
    )

    result = list(session.execute('SELECT * FROM allocations'))
    result = [(1,1,1)]