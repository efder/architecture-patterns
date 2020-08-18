from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty
        self.order_ids = [] 
    
    def allocate(self, line: OrderLine):
        # Check that if the qty is less than or equal to avaible_quantity
        if self.can_allocate(line):
            self.available_quantity -= line.qty
    
    def can_allocate(self, line: OrderLine):
        if line.sku == self.sku \
        and self.available_quantity >= line.qty \
        and line.orderid not in self.order_ids:
            self.order_ids.append(line.orderid)
            return True
        return False

class Batches:
    def __init__(self):
        self.batches = []
    
    def add_batch(self, batch: Batch):
        self.batches.append(batch)
    
    def allocate_to(self, line: OrderLine):
        selected_batch = None
        for batch in self.batches:
            if batch.can_allocate(line):
                if selected_batch is None:
                    selected_batch = batch
                else:
                    if selected_batch.eta > batch.eta:
                        selected_batch = batch
        selected_batch.allocate(line)
        return selected_batch





    