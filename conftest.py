import pytest
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, clear_mappers

from orm import metadata, start_mappers


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
        'reference TEXT,'
        'sku TEXT,'
        '_purchased_quantity INTEGER NOT NULL,'
        'eta DATE NOT NULL'
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

    # # Create the tables
    # order_lines = Table(
    #     'order_lines', metadata,
    #     Column('id', Integer, primary_key=True, autoincrement=True),
    #     Column('sku', String(255)),
    #     Column('qty', Integer, nullable=False),
    #     Column('orderid', String(255)),
    # )
    #
    # batches = Table(
    #     'batches', metadata,
    #     Column('id', Integer, primary_key=True, autoincrement=True),
    #     Column('reference', String(255)),
    #     Column('sku', String(255)),
    #     Column('_purchased_quantity', Integer, nullable=False),
    #     Column('eta', Date, nullable=True),
    # )
    #
    # allocations = Table(
    #     'allocations', metadata,
    #     Column('id', Integer, primary_key=True, autoincrement=True),
    #     Column('orderline_id', ForeignKey('order_lines.id')),
    #     Column('batch_id', ForeignKey('batches.id')),
    # )

    # metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()
