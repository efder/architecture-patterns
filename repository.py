import abc, datetime
import model

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        # Get the fields from the object
        reference = batch.reference
        eta = "null" if batch.eta is None else f'"{str(batch.eta)}"'
        sku = batch.sku
        _purchased_quantity = batch._purchased_quantity

        add_batch_query = (
            'INSERT INTO batches'
            '(reference, sku, _purchased_quantity, eta)'
            'VALUES ('
            f'"{reference}", "{sku}",  {_purchased_quantity}, {eta})'
        )

        # Add the batch object to the database
        self.session.execute(add_batch_query)

        # Get batch id
        batch_id = list(self.session.execute(f'SELECT id FROM batches WHERE reference="{reference}"'))[0][0]

        for allocation in batch._allocations:
            # Add the orderline object to the database
            add_orderline_query = (
                'INSERT INTO order_lines'
                '(sku, qty, orderid)'
                'VALUES ('
                f'"{allocation.sku}", {allocation.qty},  "{allocation.orderid}")'
            )
            self.session.execute(add_orderline_query)

            # Get the orderline id
            orderline_id = list(self.session.execute(f'SELECT id FROM order_lines '
                                                f'WHERE sku="{allocation.sku}" AND orderid="{allocation.orderid}"' ))[0][0]

            # Add the allocation to the table
            add_allocation_query = (
                'INSERT INTO allocations'
                '(orderline_id, batch_id)'
                'VALUES ('
                f'{orderline_id}, {batch_id})'
            )

            self.session.execute(add_allocation_query)

    def get(self, reference):
        batch = model.Batch(None, None, None, None)
        batches_query = f'SELECT * FROM batches WHERE reference = "{reference}"'
        batches_query_result = list(self.session.execute(batches_query))

        # Batch not found
        if len(batches_query_result) == 0:
            return None

        batch_db = batches_query_result[0]
        batch_id = batch_db[0]
        batch.reference = batch_db[1]
        batch.sku = batch_db[2]
        batch._purchased_quantity = batch_db[3]
        batch.eta = None if batch_db[4] == None else datetime.date(batch_db[4])

        # Look for the allocations and populate allocations
        orderline_ids_query = f'SELECT id FROM allocations WHERE batch_id={batch_id}'
        orderline_ids = list(map(lambda t: t[0], list(self.session.execute(orderline_ids_query))))

        # Attach orderline objects to the batch
        for orderline_id in orderline_ids:
            orderline_db = list(self.session.execute('SELECT * FROM order_lines'))[0]
            orderline = model.OrderLine(orderline_db[3], orderline_db[1], orderline_db[2])
            batch.allocate(orderline)

        return batch

    def list(self):
        batch_refs = map(lambda t: t[0], list(self.session.execute('SELECT reference FROM batches')))
        batches = list(map(lambda ref: self.get(ref), batch_refs))
        return batches