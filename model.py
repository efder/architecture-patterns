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
    
    def allocate(self, line: OrderLine):
        # Check that if the qty is less than or equal to avaible_quantity
        if line.qty <= self.available_quantity:
            self.available_quantity -= line.qty
    