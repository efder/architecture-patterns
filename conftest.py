import pytest
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, clear_mappers

@pytest.fixture
def in_memory_db():
    # Create the engine
    engine = create_engine('sqlite:///:memory:', echo=True)

    session = sessionmaker(bind=engine)()

    create_order_lines = (
        'CREATE TABLE order_lines ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'sku TEXT NOT NULL,'
        'qty INTEGER NOT NULL,'
        'orderid TEXT NOT NULL'
        ");")

    session.execute(create_order_lines)

    create_batches = (
        'CREATE TABLE batches ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'reference TEXT  NOT NULL UNIQUE,'
        'sku TEXT NOT NULL,'
        '_purchased_quantity INTEGER NOT NULL,'
        'eta DATE'
        ");"
    )

    session.execute(create_batches)

    create_allocations = (
        'CREATE TABLE allocations ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'orderline_id INTEGER NOT NULL,'
        'batch_id INTEGER NOT NULL,'
        'FOREIGN KEY(orderline_id) REFERENCES  order_lines(id),'
        'FOREIGN KEY(batch_id) REFERENCES batches(id)'
        ");"
    )

    session.execute(create_allocations)
    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()
